import datetime
import threading
from app.common.notice import sendPlusPlus, sendServerChan
from app.model.config import Config
from app.common import gxyUtils
from app.common.utils import UTC as pytz
import schedule
import logging
import time

taskList = dict()

# 启动schedule_logger的debug日志
logging.basicConfig()
schedule_logger = logging.getLogger('schedule')
schedule_logger.setLevel(level=logging.DEBUG)

# 负责调度任务
def signQueue(userId: str,type: str,sleepTime: int = 1):
    user:Config = Config.get_or_none(Config.userId == userId)
    # 检查用户配置是否合法
    if user is None:
        return False
    if user.enable is False:
        return False
    if user.planId is None or user.planId == "":
        return False
    if user.longitude is None or user.longitude == "":
        return False
    if user.latitude is None or user.latitude == "":
        return False
    if user.address is None or user.address == "":
        return False
    # 启动签到任务
    print(f"启动签到任务\t{sleepTime}")
    s = schedule.every(1).to(sleepTime).seconds.do(signTask, user,type).tag(userId,'sign')
    print(f"{userId}:{type}:{s.next_run}")
    
# 负责启动任务调度
def startTasks():
    # 选择所有启用的用户
    users : list[Config] = Config.select().where(Config.enable == True)
    # 遍历用户，启动签到任务
    for user in users:
        if user.userId not in taskList:
            tasks = []
            tasks.append(schedule.every().day.at("07:50").do(signQueue, user.userId,"START",4000).tag(user.userId,'start'))
            tasks.append(schedule.every().day.at("17:50").do(signQueue, user.userId,"END",4000).tag(user.userId,'end'))
            taskList[user.userId] = tasks
    # schedule.run_all()

# 负责停止任务调度
def stopTask(userId: str):
    if userId in taskList:
        for task in taskList[userId]:
            schedule.cancel_job(task)
        del taskList[userId]

# 取消所有任务
def stopTasks():
    for task in taskList.values():
        for t in task:
            schedule.cancel_job(t)

# 执行签到任务
def signTask(user: Config,type: str):
    # 获取签到日志
    logs = gxyUtils.getSignLogs("104609356")
    # 判断是否获取成功
    if logs!=None and len(logs) > 0:
        # 获取PRC时区的当前时间
        hourNow = datetime.datetime.now(pytz.timezone('PRC')).hour
        nowDate = str(datetime.datetime.now(pytz.timezone('PRC')))[0:10]
        # 获取最后一次签到的时间及类型
        lastSignDate = logs[0]["dateYmd"]
        lastSignType = logs[0]["type"]
        # 防止重复签到
        if lastSignDate == nowDate and lastSignType == 'END':
            return "今日签到已完成"
        if type=='END' and lastSignDate != nowDate:
            return "今日尚未上班签到"
        if type=='START' and lastSignDate == nowDate and lastSignType == 'START':
            return "今日上班签到已完成"
        # 签到并推送
        res,msg=gxyUtils.sign(user.userId, type)
        if res:
            typeStr = '上班' if type=='START' else '下班'
            title = f'工学云{typeStr}签到成功'
            content = f'工学云用户{user.phone}{typeStr}签到成功'
            if user.serverChanKey != '':
                sendServerChan(user.serverChanKey, title, content)
            if user.plusplusKey != '':
                sendPlusPlus(user.plusplusKey, title, content)

    return schedule.CancelJob


def test():
    # logs = gxyUtils.getSignLogs("104609356")
    # startTask()
    # if '104609356' in taskList:
        # for task in taskList['104609356']:
            # print(task.next_run)
        # taskList['104609356'][1].run()
    s = taskList['104609356']
    s[0].run()
    print(111)
    
    # schedule.every(5).seconds.do(signQueue, "104609356").tag("104609356",'end')