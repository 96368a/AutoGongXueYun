import schedule

# from app.common.gxyUtils import sign

# sign('104609356','123456')

# from app.common.task import startTask

# startTask()

# while True:
#     schedule.run_pending()
    # time.sleep(1)
def signQueue(id):
    print(id)
schedule.every().day.at("21:53").do(signQueue, "测试任务1").tag("测试任务1",'start')