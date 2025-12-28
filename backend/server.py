from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse
from pydantic import BaseModel
from datetime import date
from render import render_top10
from storage import load_items, save_items  # 你需要在 storage.py 里加 save_items
from fastapi.staticfiles import StaticFiles

import os
import uuid

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
app = FastAPI()
STATIC_DIR = os.path.join(BASE_DIR, "static")
app.mount("/ui", StaticFiles(directory=STATIC_DIR, html=True), name="ui")


BASE_DIR = os.path.dirname(os.path.abspath(__file__))
OUT_PATH = os.path.join(BASE_DIR, "..", "output", "top10.png")

@app.get("/")
def home():
    return {"ok": True, "try": ["/items", "/top10.png", "/docs"]}


@app.get("/items")
def list_items():
    items = load_items()
    return{
        "items": [
            {
                "id": it["id"],
                "name": it["name"],
                "date_in": it["date_in"].isoformat(),
            }
            for it in items
        ]
    }

class ItemCreate(BaseModel):
    name: str
    date_in: date | None = None  # 不传就默认今天

@app.post("/items")
def add_item(body: ItemCreate):
    items = load_items()

    new_item = {
        "id": str(uuid.uuid4()),
        "name": body.name.strip(),
        "date_in": body.date_in or date.today(),
    }

    items.append(new_item)
    save_items(items)

    return {
        "ok": True,
        "item": {
            "id": new_item["id"],
            "name": new_item["name"],
            "date_in": new_item["date_in"].isoformat(),
        },
    }

@app.delete("/items/{item_id}")
def delete_item(item_id: str):
    items = load_items()
    before = len(items)
    items = [it for it in items if it["id"] != item_id]

    if len(items) == before:
        raise HTTPException(status_code=404, detail="item not found")

    save_items(items)
    return {"ok": True}


@app.get("/top10.png")
def top10_png():
    items = load_items()
    os.makedirs(os.path.dirname(OUT_PATH), exist_ok=True)
    render_top10(items, OUT_PATH)
    return FileResponse(OUT_PATH, media_type="image/png")

