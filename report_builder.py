import os
import json
import uuid
import pandas as pd

REPORTS_DIR = "reports"
BASE_URL = os.getenv("BASE_URL", "http://localhost:5000/reports")
TEMPLATE_PATH = os.path.join(os.path.dirname(__file__), "..", "templates", "dashboard.html")
os.makedirs(REPORTS_DIR, exist_ok=True)


async def build_report(file_path: str, file_name: str, ai_result: dict) -> str:
    ext = os.path.splitext(file_path)[1].lower()
    df = pd.read_csv(file_path) if ext == ".csv" else pd.read_excel(file_path)

    raw_data = df.to_json(orient="records", force_ascii=False, date_format="iso")
    ai_config = json.dumps(ai_result, ensure_ascii=False)
    insight = ai_result.get("insights", "")

    with open(TEMPLATE_PATH, "r", encoding="utf-8") as f:
        template = f.read()

    html = (template
        .replace("{{FILE_NAME}}", file_name)
        .replace("{{INSIGHT}}", insight)
        .replace("{{RAW_DATA}}", raw_data)
        .replace("{{AI_CONFIG}}", ai_config)
    )

    report_id = str(uuid.uuid4())[:8]
    report_path = os.path.join(REPORTS_DIR, f"{report_id}.html")
    with open(report_path, "w", encoding="utf-8") as f:
        f.write(html)

    return f"{BASE_URL}/{report_id}.html"
