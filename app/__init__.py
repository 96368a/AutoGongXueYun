from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from starlette.exceptions import HTTPException as StarletteHTTPException
from fastapi.exception_handlers import (
    http_exception_handler,
)
from starlette.responses import FileResponse
import os

app = FastAPI()
origins = [
    "http://localhost:5173",
    "http://localhost:4000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.exception_handler(StarletteHTTPException)
async def custom_http_exception_handler(request, exc):
    print(f"OMG! An HTTP error!: {repr(exc)}")
    if exc.status_code == 404 and not request.url.path.startswith("/api"):
            # try open file for path
        file_path = os.path.join("web/dist", request.url.path.strip("/"))
        if os.path.isfile(file_path):
            return FileResponse(file_path)
        return FileResponse('web/dist/index.html')
    return await http_exception_handler(request, exc)

# app.mount("/assets", StaticFiles(directory="web/dist/assets"), name="assets")

# 初始化路由
from app import router