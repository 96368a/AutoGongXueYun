import schedule
import threading
import time
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from starlette.exceptions import HTTPException as StarletteHTTPException
from fastapi.exception_handlers import (
    http_exception_handler,
)
from starlette.responses import FileResponse
import os
from app.common.task import startTasks, stopTasks
    
app = FastAPI()
origins = [
    "http://localhost:5173",
    "http://localhost:4000",
]
stop_run_continuously = None
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.exception_handler(StarletteHTTPException)
async def custom_http_exception_handler(request, exc):
    # print(f"OMG! An HTTP error!: {repr(exc)}")
    if exc.status_code == 404 and not request.url.path.startswith("/api"):
            # try open file for path
        file_path = os.path.join("web/dist", request.url.path.strip("/"))
        if os.path.isfile(file_path):
            return FileResponse(file_path)
        return FileResponse('web/dist/index.html')
    return await http_exception_handler(request, exc)

# app.mount("/assets", StaticFiles(directory="web/dist/assets"), name="assets")

# 初始化路由
from app.controller import base,user,common

# 初始化日志
from app.common import logger
# 定时任务
def run_continuously(interval=1):
    cease_continuous_run = threading.Event()

    class ScheduleThread(threading.Thread):
        @classmethod
        def run(cls):
            while not cease_continuous_run.is_set():
                schedule.run_pending()
                time.sleep(interval)

    continuous_thread = ScheduleThread()
    continuous_thread.start()
    return cease_continuous_run

# 启动签到任务调度
@app.on_event("startup")
async def startup_event():
    global stop_run_continuously
    stop_run_continuously = run_continuously()
    startTasks()
    
# 关闭所有线程
@app.on_event("shutdown")
async def shutdown_event():
    global stop_run_continuously
    stop_run_continuously.set()
    