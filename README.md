# 前人栽树后人乘凉
此代码根据kangarooking/fastgpt-dify-adapter修改而来，感谢这位兄弟

# getbiji-dify-adapter
Dify外接得到Get笔记知识库的工具

# **📌 `.env` 配置文件说明**
本文件用于配置 **得到Get笔记知识库 Dify 适配器** 的环境变量，所有运行时参数均可通过 `.env` 配置，无需修改代码。  
适用于 **Docker部署** 和 **本地开发**，确保灵活性和可维护性。

---

## **📖 变量配置说明**
以下是所有可用的环境变量及其作用：

### **🌐 1. 服务器配置**
| 变量 | 说明 | 默认值 |
|------|------|-------|
| `PORT` | Flask 服务器运行端口 | `6000` |
| `GUNICORN_WORKERS` | Gunicorn 进程数（提升并发） | `2` |
| `GUNICORN_TIMEOUT` | Gunicorn 超时时间（秒） | `60` |

📌 **示例：**
```ini
PORT=6000
GUNICORN_WORKERS=2
GUNICORN_TIMEOUT=60
```

---

### **🤖 3. Get笔记 相关配置**
| 变量 | 说明                                                            | 默认值 |
|------|---------------------------------------------------------------|----|
| `GETBIJI_BASE_URL` | 得到Get笔记 基础 API 地址    | `https://open-api.biji.com/getnote/openapi` |
| `GETBIJI_TIMEOUT` | 得到Get笔记 API 请求超时时间（秒）       | `30` |
| `DATASET_INTENT_REWRITE` | 是否开启问题优化 (`true/false`)    | `true` |
| `DATASET_SELECT_MATRIX` | 是否使用 Get笔记 重新排序（ReRank）（`true/false`）   | `true` |

📌 **示例：**
```ini
GETBIJI_BASE_URL=https://open-api.biji.com/getnote/openapi
GETBIJI_TIMEOUT=30
DATASET_INTENT_REWRITE=true
DATASET_SELECT_MATRIX=true
```

---

### **📜 4. 日志 & 调试**
| 变量 | 说明 | 默认值 |
|------|------|-------|
| `LOG_LEVEL` | 日志级别 (`DEBUG, INFO, WARNING, ERROR, CRITICAL`) | `INFO` |

📌 **示例：**
```ini
LOG_LEVEL=DEBUG
```

---

## **🚀 `.env` 文件完整示例**
```ini
# =========================================
# 🌐 服务器配置
# =========================================
# Flask 运行端口（必须与 docker-compose 端口一致）
PORT=6000

# Gunicorn 配置（提高并发能力）
GUNICORN_WORKERS=2   # Gunicorn 工作进程数
GUNICORN_TIMEOUT=60  # Gunicorn 超时时间（秒）

# =========================================
# 🤖 Get笔记 相关配置
# =========================================
# Get笔记 基础 API 地址
GETBIJI_BASE_URL=https://open-api.biji.com/getnote/openapi

# Get笔记 API 请求超时时间（秒）
GETBIJI_TIMEOUT=30

# 是否开启问题优化（true/false）
DATASET_INTENT_REWRITE=true

# 是否使用 Get笔记 重新排序（ReRank）（true/false）
DATASET_SELECT_MATRIX=true

# =========================================
# 📜 日志 & 调试
# =========================================
# 日志级别（DEBUG, INFO, WARNING, ERROR, CRITICAL）
LOG_LEVEL=INFO
```

---

## **🔧 使用 `.env` 配置**
### **🔹 1. 在 Docker 中使用**
在 `docker-compose.yml` 中**自动加载 `.env` 文件**：
```yaml
version: '3'

services:
  getbiji-dify-adapter:
    container_name: getbiji-dify-adapter
    image: yufeiyohi/getbiji-dify-adapter:latest
    env_file:
      - .env
    ports:
      - "${PORT}:${PORT}"
    restart: unless-stopped
```

---

### **🔹 2. 在 Python 代码中使用**
确保 `python-dotenv` 已安装：
```bash
pip install python-dotenv
```

然后，在 Flask 代码中加载 `.env`：
```python
from dotenv import load_dotenv
import os

# 加载 .env 文件
load_dotenv()

# 读取环境变量
PORT = int(os.getenv('PORT', 6000))

print(f"PORT: {PORT}")
```

---

## **🎯 结论**
✅ **所有配置均可通过 `.env` 进行管理，无需修改代码**  
✅ **适用于 Docker & 本地开发，增强灵活性**  
✅ **支持得到Get笔记 配置、日志级别、服务器参数**  

🚀 **现在，你可以快速配置和管理 得到Get笔记 Dify 适配器！** 🚀