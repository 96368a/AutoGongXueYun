import threading
import time
import uvicorn
from app import app
import task
import schedule

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
    
