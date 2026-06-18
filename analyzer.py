import os
import json
import httpx
import pandas as pd

# ضع الـ API Key هنا
GROQ_API_KEY = "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"

GROQ_MODEL = "llama-3.3-70b-versatile"

SYSTEM_PROMPT = """أنت محلل بيانات متخصص. مهمتك هي فهم البيانات المرسلة إليك وإرجاع JSON فقط يحدد أفضل طريقة لعرضها.

قواعد مهمة:
- رد بـ JSON فقط، بدون أي كلام أو شرح
- اختر الشارتس الأنسب للبيانات فعلاً
- لا تختر أكثر من 4 شارتس
- الـ insights جملة واحدة مفيدة بالعربي
- تأكد أن أسماء الأعمدة مطابقة تماماً للبيانات المرسلة

الـ JSON المطلوب بالضبط:
{
  "insights": "جملة تحليلية واحدة عن أبرز نمط في البيانات",
  "metrics": [
    {"label": "اسم المقياس", "column": "اسم العمود", "operation": "sum|avg|count|max|min"}
  ],
  "charts": [
    {
      "type": "bar|line|pie|scatter",
      "title": "عنوان الشارت",
      "x_column": "اسم العمود",
      "y_column": "اسم العمود أو null",
      "color_column": "اسم العمود أو null"
    }
  ]
}"""


async def analyze_file(file_path: str, focus: str = None) -> dict:
    ext = os.path.splitext(file_path)[1].lower()

    if ext == ".csv":
        df = pd.read_csv(file_path)
    else:
        df = pd.read_excel(file_path)

    preview = df.head(15).to_json(
        orient="records",
        force_ascii=False
    )

    columns_info = {
        col: str(df[col].dtype)
        for col in df.columns
    }

    total_rows = len(df)

    focus_text = (
        f"\nركز على: {focus}"
        if focus
        else "\nحلل كل البيانات تلقائياً"
    )

    user_message = f"""البيانات:

إجمالي الصفوف: {total_rows}

الأعمدة وأنواعها:
{json.dumps(columns_info, ensure_ascii=False)}

أول 15 صف:
{preview}

{focus_text}
"""

    async with httpx.AsyncClient(timeout=120) as client:
        response = await client.post(
            "https://api.groq.com/openai/v1/chat/completions",
            headers={
                "Authorization": f"Bearer {GROQ_API_KEY}",
                "Content-Type": "application/json"
            },
            json={
                "model": GROQ_MODEL,
                "temperature": 0.1,
                "response_format": {
                    "type": "json_object"
                },
                "messages": [
                    {
                        "role": "system",
                        "content": SYSTEM_PROMPT
                    },
                    {
                        "role": "user",
                        "content": user_message
                    }
                ]
            }
        )

    response.raise_for_status()

    raw = response.json()

    text = raw["choices"][0]["message"]["content"]

    try:
        result = json.loads(text)
    except:
        text = (
            text.replace("```json", "")
            .replace("```", "")
            .strip()
        )
        result = json.loads(text)

    return result
