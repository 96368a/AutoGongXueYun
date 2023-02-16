import schedule

# from app.common.gxyUtils import sign

# sign('104609356','123456')

# from app.common.task import startTask

# startTask()

# while True:
#     schedule.run_pending()
    # time.sleep(1)
print("启动测试")
from app.common import task
# def signQueue(id):
#     print(id)
task.test()
# id = "测试任务1"
# schedule.every().day.at("21:56").do(signQueue, id).tag(id,'start')