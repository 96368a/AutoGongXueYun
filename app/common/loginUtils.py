from app.common.captcha import getCode
import uuid
from app.common.utils import encrypt
import time
import requests
import json
from app.model.config import create_or_update as createConfig

def loginUser(phone, password):
    uuidStr = str(uuid.uuid4())
    # 获取一个验证码
    captcha = getCode(uuidStr)
    for i in range(5):
        # 验证码位数不对，重新获取
        if len(captcha) == 5:
            break
        elif i == 4:
            # 5次都不对，返回错误
            return {"code": "400", "msg": "验证码获取失败，请重试"}
        captcha = getCode(uuidStr)
    headers = {
        "roleKey": "student",
        "host": "api.moguding.net:9000",
        "origin": "https://api.moguding.net",
        "referer": "https://api.moguding.net/",
        "content-type": "application/json; charset=UTF-8",
    }
    datas = {"t": encrypt(str(int(time.time() * 1000))),
             "phone": encrypt(phone),
             "password": encrypt(password),
             "captcha": captcha,
             "loginType": "web",
             "uuid": uuidStr
             }
    res = requests.post('https://api.moguding.net:9000/session/user/v3/login',
                        headers=headers,data=json.dumps(datas),verify=False)
    data = res.json()
    if data["code"] == 200:
        # return data
        data1 = data["data"]
        createConfig(phone, password, data1["token"], data1["userId"])
    return data

def loginCycle(phone,password):
    # 登录3次,如果3次都失败,则返回错误
    for i in range(3):
        data = loginUser(phone, password)
        # 登录成功或者不是验证码错误,则返回
        if data["code"] == 200 or data["code"] != 522:
            return data
        elif i == 4:
            return {"code": "400", "msg": "登录失败，请重试"}
        else:
            time.sleep(1)