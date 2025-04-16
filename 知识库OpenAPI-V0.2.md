**知识库 OpenAPI-V0.1**

**知识库接口说明**

**一、接口基本信息**

接口地址：https://open-api.biji.com/getnote/openapi

鉴权方式：基于**OAuth 2.0** 认证机制的 **Bearer Token Authentication**（Bearer 令牌认证）

**示例**

|Bash<br>curl --location --request POST 'https://open-api.biji.com/getnote/openapi' \<br>--header 'Content-Type: application/json' \<br>--header 'Connection: keep-alive' \<br>--header 'Authorization: Bearer {api-key}' \<br>--header 'X-OAuth-Version: 1' \<br>--data-raw '{}|
| :- |

**二、接口明细说明**

1. **知识库召回**


| **接口地址：**/knowledge/search/recall<br />**请求方法：**POST |
| :----------------------------------------------------------- |

**参数说明**

|字段|类型|说明|是否必须|示例|备注|
| :- | :- | :- | :- | :- | :- |
|question|string|问题|是|||
|topic\_ids|[]string|知识库ID列表|是||当前只支持1个|
|intent\_rewrite|bool|问题意图重写|是|true|默认：false|
|select\_matrix|bool|对结果进行重选|否|true|默认：false|
|<p>history</p><p></p>|[]struct{"content":"能进一步说明吗","role": "USER"}|<p>搜索记录</p><p></p>|否||用于追问|

**请求示例**

```curl
curl --location --request POST 'https://open-api.biji.com/getnote/openapi/knowledge/search/recall' \
--header 'Content-Type: application/json' \
--header 'Connection: keep-alive' \
--header 'Authorization: Bearer {api-key}' \
--header 'X-OAuth-Version: 1' \
--data-raw '{
    "question": "举个具体的例子呢",
    "topic_ids": [
        "WPexDor795JvYzva03w16pkmMZVyN4"
    ],
    "history": [
        {
            "content": "黑洞是什么",
            "role": "user"
        },
        {
            "content": "是一款产品",
            "role": "assistant"
        }
    ],
    "intent_rewrite": false,
    "select_matrix": false
}'
```

**响应示例**

|字段|类型|说明|备注|
| :- | :- | :- | :- |
|id|string|召回对应资源ID||
|title|string|召回对应资源标题|可能为空|
|content|string|召回内容|默认：false|
|score|float|得分||
|type|string|召回资源类型|FILE：文件<br />NOTE：笔记<br />BLOGGER：订阅博主或直播|
|recall\_source|string|召回来源|embedding<br />keyword|

```
{
    "h": {
        "c": 0,
        "e": "",
        "s": 1741253826,
        "t": 2099,
        "apm": "4962fec80013253"
    },
    "c": {
        "data": [
            {
                "id": "PAO/hakxI/mel6b+g+SuCA==",
                "title": "一口气了解关税 #关税 #掘金计划2025 #一口气看懂经济学 #经济学知识看世界",
                "content": "📈 关税的基本概念与运行机制。以“奶茶国”和“奶牛国”为例，奶茶国对进口奶粉加征20%关税，进口商为维持利润提高售价，这就是关税基本运行机制。👍 关税对本国的利弊。好处：政府创收：如美国对进口洗衣机征税，三年获约十亿美元收入。保护本国产业：幼稚产业保护理论，美、德曾保护纺织等产业，中国曾高关税扶持汽车产业，印度提高关税保护制造业。获得民意支持：经济下行时更明显，且美国摇摆州关键产业工会影响关税政策。作为谈判筹码：特朗普常用此手段，如退出北美自贸协定加征关税后重新谈判获更多保护条款。缩小贸易逆差：短期理论上可行，但实际影响复杂。政府创收：如美国对进口洗衣机征税，三年获约十亿美元收入。保护本国产业：幼稚产业保护理论，美、德曾保护纺织等产业，中国曾高关税扶持汽车产业，印度提高关税保护制造业。",
                "score": 0.09380767438923665,
                "type": "NOTE",
                "recall_source": "embedding"
            },
            {
                "id": "PAO/hakxI/mel6b+g+SuCA==",
                "title": "【完整纯享版】一口气了解通胀",
                "content": "📈 通胀现象与案例。1923年德国出现恶性通胀，纸币贬值严重，物价每两天翻一番，年化通胀率达1.5%×10的56次方。2008年津巴布韦印出100万亿津巴布韦元纸币，物价每24.7小时翻一倍，年化通胀率达7.3%×10的108次方。1946年匈牙利物价每15.6小时翻一倍，年化通胀率为7.5×10的170次方。2022年，美国、欧盟、英国通胀飙升，通胀再次成为全球经济主题。📊 通胀衡量指标与各国情况。衡量通胀常用指标是CPI（消费者物价指数），反映商品和服务物价走势。美国60年间物价涨了约10倍；国内通胀效应明显；澳大利亚物价翻了16倍，英国翻了25倍，印度翻了88倍，土耳其翻了970万倍。🧐 通胀形成原因与本质。",
                "score": 0.07456002020546793,
                "type": "BLOGGER",
                "recall_source": "embedding"
            },
            {
                "id": "PAO/hakxI/mel6b+g+SuCA==",
                "title": "三维菁彩声技术白皮书",
                "content": "在通过对象输出接口请求对象音频数据和元数据的输出的情况下，绕过漫反射处理提供元数据和音频 数据的输入。元数据以 objectsTypemetadata对象的输入形式进入渲染器；通过对元素元数据预处理模块的 处理，经过 objects_gains计算，获得基于对象内容的元数据和音频数据的输出， 当请求接口输出数据时， 这些元素将启用以进行播放。\n16\nAudio Vivid技术白皮书\n2.基于声道的渲染\n[基于声道 DirectSpeakers的渲染原理如下：\n图 9 基于声道的渲染]M+000 M+030 M-000 Ch1 GainCalculatorDirectSpeakers M+045 直接扬声器增益计算 Ch2 M-045 GY/T316 输入 Ch3 M+090 _layout 扬声器 M-090 布局 M+135 M-135 Chx UH+180 LFE1 LFE2",
                "score": 0.009718604104047488,
                "type": "FILE",
                "recall_source": "embedding"
            },
            {
                "id": "PAO/hakxI/mel6b+g+SuCA==",
                "title": "#一口气读懂经济学",
                "content": "导致企业家与打工人、大企业与小企业贫富差距拉大，很多美国人体感不明显。💱 货币政策与降息预期。美联储关注通胀和失业率，目前通胀稳定，焦点在失业率，11月为4.2%，低于4.5%大概率不影响降息节奏。此次降息不像之前加息那样引发全球资本巨浪，降息空间约100个基点。👑 特朗普2.0时代政策展望。提及接下来特朗普2.0时代可能的政策，但未具体阐述。",
                "score": 0.009242766772194181,
                "type": "BLOGGER",
                "recall_source": "embedding"
            }
        ]
    }
}
```



