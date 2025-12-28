import json
import os
import uuid
from datetime import date

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
JSON_PATH = os.path.join(BASE_DIR, "..", "data", "items.json")

def load_items() -> list[dict]:
    if not os.path.exists(JSON_PATH):
        # 如果文件不存在，自动创建一个空库
        os.makedirs(os.path.dirname(JSON_PATH), exist_ok=True)
        with open(JSON_PATH, "w", encoding="utf-8") as f:
            json.dump({"items": []}, f, ensure_ascii=False, indent=2)

    with open(JSON_PATH, "r", encoding="utf-8") as f:
        db = json.load(f)

    items = []
    changed = False

    for it in db["items"]:
        if "id" not in it:
            it["id"] = str(uuid.uuid4())
            changed = True
    
        items.append({
            "id": it["id"],
            "name": it["name"],
            "date_in": date.fromisoformat(it["date_in"]),
        })

    if changed:
        with open(JSON_PATH, "w", encoding="utf-8") as f:
            json.dump(db, f, ensure_ascii=False, indent=2)
    return items

def save_items(items: list[dict]) -> None:
    # date 对象写不进 JSON，所以转成字符串
    payload = {
        "items": [
            {
                "id": it["id"],
                "name": it["name"],
                "date_in": it["date_in"].isoformat(),
            }
            for it in items
        ]
    }
    os.makedirs(os.path.dirname(JSON_PATH), exist_ok=True)
    with open(JSON_PATH, "w", encoding="utf-8") as f:
        json.dump(payload, f, ensure_ascii=False, indent=2)