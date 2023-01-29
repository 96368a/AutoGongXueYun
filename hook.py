import requests
import pickle
import datetime
import MessagePush
import sys
import time
import json
from app.common.utils import AES, UTC as pytz
from main import parseUserInfo, prepareSign, signCheck as Check, getToken, getUserAgent, encrypt
import base64
import schedule
import threading
import random

def sign(user, sleepTime=0):
    time.sleep(sleepTime)
    # 用户配置未启用每日签到
    if not user["enable"]:
        return

    url = "https://api.moguding.net:9000/attendence/clock/v1/list"
    if user["keepLogin"]:
        print('          此用户保持登录状态开启，准备使用Token查询          ')
        token = user["token"]
    else:
        print('            此用户保持登录状态关闭，准备登录账号          ')
        token = getToken(user)["data"]["token"]
    header = {
        "content-type": "application/json;charset=UTF-8",
        "rolekey": "student",
        "host": "api.moguding.net:9000",
        "authorization": token,
        "user-agent": getUserAgent(user)
    }
    t = str(int(time.time() * 1000))
    data = {
        "t": encrypt("23DbtQHR2UMbH6mJ", t),
        "currPage": 1,
        "pageSize": 2,
        "planId": user["planId"],
    }
    res = requests.post(url=url, headers=header, data=json.dumps(data))

    if res.json()["msg"] != 'success':
        print('            获取用户打卡记录失败          ')
        return

    lastSignInfo = res.json()["data"][0]
    lastSignDate = lastSignInfo["dateYmd"]
    lastSignType = lastSignInfo["type"]
    hourNow = datetime.datetime.now(pytz.timezone('PRC')).hour
    nowDate = str(datetime.datetime.now(pytz.timezone('PRC')))[0:10]
    if hourNow <= 12 and lastSignType == 'END' and lastSignDate != nowDate:
        print('            今日未打上班卡，准备签到          ')
        prepareSign(user)
    elif lastSignType == 'START' and lastSignDate == nowDate:
        print('            今日未打下班卡，准备签到          ')
        prepareSign(user)
    else:
        MessagePush.pushMessage(user['phone'], '今日签到已完成！',
                                '用户：' + user['phone'] + '今日签到已完成！',
                                user["pushKey"])


def work():
    users = parseUserInfo()
    print('----------------------------每日签到检查开始-----------------------------')
    try:
        for user in users:
            sleepTime = random.randint(0, 3)
            thread = threading.Thread(target=sign, args=(user, sleepTime))
            thread.start()
    except Exception as e:
        print('每日签到检查运行错误！可能与服务器建立连接失败,具体错误原因：' + str(e))
    print('----------------------------每日签到检查完成-----------------------------')


if __name__ == '__main__':
    work()
    schedule.every().day.at("08:00").do(work)
    schedule.every().day.at("18:00").do(work)
    schedule.every().day.at("21:20").do(work)
    while True:
        schedule.run_pending()
