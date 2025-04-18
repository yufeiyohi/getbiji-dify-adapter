import os
import json
import time
import requests
import logging
from flask import Flask, request, jsonify
from dotenv import load_dotenv

# 加载环境变量
load_dotenv()

# 配置日志
LOG_LEVEL = os.getenv('LOG_LEVEL', 'INFO').upper()
logging.basicConfig(
    level=getattr(logging, LOG_LEVEL, logging.INFO),
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Flask 应用
app = Flask(__name__)

# 读取环境变量
GETBIJI_BASE_URL = os.getenv('GETBIJI_BASE_URL', 'https://open-api.biji.com/getnote/openapi')
GETBIJI_TIMEOUT = int(os.getenv('GETBIJI_TIMEOUT', 30))  # GETBiji API 超时
DATASET_INTENT_REWRITE = os.getenv('DATASET_INTENT_REWRITE', 'false').lower() == 'true'
DATASET_SELECT_MATRIX = os.getenv('DATASET_SELECT_MATRIX', 'true').lower() == 'true'

def validate_api_key(auth_header):
    """验证 API 密钥"""
    if not auth_header or not auth_header.startswith('Bearer '):
        return False
    return True  # 只要格式正确就通过验证

@app.route('/retrieval', methods=['POST'])
def retrieval():
    start_time = time.time()
    client_ip = request.remote_addr
    logger.info(f'收到检索请求，IP: {client_ip}')

    # 验证 API 认证
    auth_header = request.headers.get('Authorization')
    if not validate_api_key(auth_header):
        logger.warning(f'API 认证失败，IP: {client_ip}')
        return jsonify({'error_code': 1002, 'error_msg': '授权失败'}), 403

    # 检查Content-Type
    if not request.content_type or 'application/json' not in request.content_type:
        logger.error(f'无效的Content-Type: {request.content_type}')
        return jsonify({'error_code': 400, 'error_msg': 'Content-Type必须是application/json'}), 400

    # 解析请求 JSON
    try:
        raw_data = request.get_data(as_text=True)
        if not raw_data.strip():
            logger.error('请求体为空')
            return jsonify({'error_code': 400, 'error_msg': '请求体不能为空'}), 400
            
        dify_request = request.get_json(force=True)
        logger.info(f'Dify 请求参数: {json.dumps(dify_request, ensure_ascii=False)}')
    except json.JSONDecodeError as e:
        logger.error(f'JSON 解析失败: {str(e)}，原始请求体: {raw_data[:200]}...')
        return jsonify({
            'error_code': 400,
            'error_msg': f'无效的JSON格式: {str(e)}'
        }), 400
    except Exception as e:
        logger.error(f'请求处理失败: {str(e)}')
        return jsonify({'error_code': 400, 'error_msg': '请求处理失败'}), 400

    # 提取参数
    query = dify_request.get('query')
    knowledge_id = dify_request.get('knowledge_id')
    retrieval_setting = dify_request.get('retrieval_setting', {})
    metadata_condition = dify_request.get('metadata_condition', {})
    history = dify_request.get('history', [])

    if not knowledge_id or not query:
        logger.error('缺少必要参数 knowledge_id 或 query')
        return jsonify({'error_code': 400, 'error_msg': '缺少必要参数'}), 400

    # 查询参数
    top_k = retrieval_setting.get('top_k', 10)
    score_threshold = retrieval_setting.get('score_threshold', 0.5)

    # 构建知识库API请求
    knowledge_request = {
        'question': query,
        'topic_ids': [knowledge_id],
        'intent_rewrite': DATASET_INTENT_REWRITE,
        'select_matrix': DATASET_SELECT_MATRIX,
        'history': history
    }

    # 处理metadata_condition过滤
    if metadata_condition:
        conditions = metadata_condition.get('conditions', [])
        logical_operator = metadata_condition.get('logical_operator', 'and')
        
        if conditions:
            knowledge_request['metadata_filters'] = {
                'logical_operator': logical_operator,
                'conditions': conditions
            }

    headers = {
        'Authorization': auth_header,
        'Content-Type': 'application/json',
        'Connection': 'keep-alive',
        'X-OAuth-Version': '1'
    }
    knowledge_url = f"{GETBIJI_BASE_URL}/knowledge/search/recall"
    
    # 发送请求（支持指数退避策略）
    max_retries = 3
    for attempt in range(max_retries):
        try:
            response = requests.post(knowledge_url, headers=headers, json=knowledge_request, timeout=GETBIJI_TIMEOUT)
            if response.status_code == 200:
                knowledge_response = response.json()
                logger.info(f'知识库API 响应成功，耗时: {time.time() - start_time:.2f}s')
                return jsonify(format_knowledge_response(knowledge_response))
            
            elif response.status_code in {401, 403}:
                logger.warning(f'知识库API 认证失败，IP: {client_ip}')
                return jsonify({'error_code': 1002, 'error_msg': '授权失败'}), 403

            logger.error(f'知识库API 错误: {response.status_code}，内容: {response.text}')
            return jsonify({'error_code': 500, 'error_msg': f'知识库API 错误 {response.status_code}'}), 500

        except requests.exceptions.RequestException as e:
            logger.error(f'知识库API 请求失败: {str(e)}，第 {attempt+1} 次重试')
            time.sleep(2 ** attempt)  # 指数退避策略

    return jsonify({'error_code': 500, 'error_msg': '知识库API 请求失败'}), 500

def format_knowledge_response(knowledge_response):
    """格式化知识库API响应为Dify格式"""
    records = []
    data_list = knowledge_response.get('c', {}).get('data', [])

    for item in data_list:
        if not isinstance(item, dict):
            logger.warning(f'跳过非字典类型数据: {item}')
            continue

        # 构建metadata对象
        metadata = {
            'path': f"knowledge://{item.get('id', '')}",
            'type': item.get('type', ''),
            'recall_source': item.get('recall_source', ''),
            'id': item.get('id', '')
        }

        records.append({
            'content': item.get('content', ''),
            'score': item.get('score', 0),
            'title': item.get('title', 'Unknown'),
            'metadata': metadata
        })

    return {'records': records}

if __name__ == '__main__':
    port = int(os.getenv('PORT', 6000))
    app.run(host='0.0.0.0', port=port)