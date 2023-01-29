from fastapi import FastAPI


app = FastAPI()

# 初始化路由
from app import router

@app.get("/items/")
async def read_items(q: str):
    results = {"items": [{"item_id": "Foo"}, {"item_id": "Bar"}]}
    if q:
        results.update({"q": q})
    return results