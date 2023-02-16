import threading
import time
import uvicorn
from app import app
from app.common.gxyUtils import testNetword
# import task
import schedule
import os
import config

# 配置代理
if config.proxy:
    os.environ['http_proxy'] = config.proxy
    os.environ['https_proxy'] = config.proxy
# 检查网络
res,data = testNetword()
if res:
    print("连接工学云服务器正常~")
else:
    if config.proxy:
        print("代理服务器不可用，请检查代理配置")
    else:
        print("连接工学云服务器失败，请尝试配置代理")
    exit(0)


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

if __name__ == "__main__":
    from app.model import config
    # config.test()
    stop_run_continuously = run_continuously()
    uvicorn.run(app, host="0.0.0.0", port=8000)
    
