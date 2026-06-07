import json
from generate import stream_generate

SKUS = ["BZH", "BYH", "BXH"]

ALLOWED_FIELDS = [
    "作業系統", "中央處理器", "顯示晶片", "顯示器", "記憶體", "儲存裝置",
    "鍵盤種類", "連接埠", "音效", "通訊", "視訊鏡頭", "安全裝置",
    "電池", "變壓器", "尺寸", "重量", "顏色"
]


def llm_parse_query(query: str):

    prompt = f"""
You are a classifier. Your goal is tring to retrieve the SKUs and field of the questions. 
If there are no corresponding field, please answer with "NULL".
Else, please answer with JSON format

Allowed SKUs:
{SKUS}

Allowed fields:
{ALLOWED_FIELDS}

Example:

* Question: 型號 BZH 的 CPU 是什麼？
* Answer: 
{{
  "skus": ["BZH"],
  "field": "中央處理器"
}}

* Question: Which one has the powerfull battery?
* Answer: 
{{
  "skus": ["BZH", "BYH", "BXH"],
  "field": "電池"
}}

User query:
{query}
"""

    raw = stream_generate(prompt)["text"]

    try:
        return json.loads(raw)
    except:
        return {
            "skus": [],
            "field": None,
            "task": "semantic"
        }