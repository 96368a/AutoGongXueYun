from app.common.captcha import getCode
import uuid
from app.common.utils import encrypt, getSign
import time
import requests
import json
from app.model.config import Config, create_or_update as createConfig


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
                        headers=headers, data=json.dumps(datas), verify=False)
    data = res.json()
    if data["code"] == 200:
        # return data
        data1 = data["data"]
        createConfig(phone, password, data1["token"], data1["userId"])
    return data


def loginCycle(phone, password):
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


def refreshLogin(phone: str):
    user = Config.get_or_none(Config.phone == phone)
    if user is None:
        return {"code": "400", "msg": "用户不存在"}
    user = user.__data__
    url = "https://api.moguding.net:9000/practice/quality/report/v1/existScore"
    headers = {
        "roleKey": "student",
        "host": "api.moguding.net:9000",
        "origin": "https://api.moguding.net",
        "referer": "https://api.moguding.net/",
        "content-type": "application/json; charset=UTF-8",
        "Authorization": user["token"]
    }
    body = {
        "t": encrypt(str(int(time.time() * 1000))),
    }
    res = requests.post(url, headers=headers,
                        data=json.dumps(body), verify=False)
    data = res.json()
    if data["code"] == 401:
        # token失效,重新登录
        data = loginCycle(user["phone"], user["password"])
        return data

def getSignLogs(userId: str):
    user:Config = Config.get_or_none(Config.userId == userId)
    if user is None:
        return None
    refreshLogin(user.phone)
    url = "https://api.moguding.net:9000/attendence/clock/v1/list"
    header = {
        "content-type": "application/json;charset=UTF-8",
        "rolekey": "student",
        "host": "api.moguding.net:9000",
        "authorization": user.token
    }
    t = str(int(time.time() * 1000))
    data = {
        "t": encrypt(t),
        "currPage": 1,
        "pageSize": 2,
        "planId": user.planId,
    }
    res = requests.post(url=url, headers=header, data=json.dumps(data))

    if res.json()["msg"] != 'success':
        return None
    return res.json()["data"]
    
def sign(userId: str, signType: str):
    user: Config = Config.get_or_none(Config.userId == userId)
    if user is None:
        return {"code": "400", "msg": "用户不存在"}

    text = user.type + signType + user.planId + userId + user.address

    headers2 = {
        'roleKey': 'student',
        "user-agent": user.userAgent,
        "sign": getSign(text=text),
        "authorization": user.token,
        "content-type": "application/json; charset=UTF-8"
    }
    data = {
        "country": user.country,
        "address": user.address,
        "province": user.province,
        "city": user.city,
        "area": user.area,
        "latitude": user.latitude,
        "longitude": user.longitude,
        "description": user.desc,
        "planId": user.planId,
        "type": signType,
        "device": user.type,
    }
    url = "https://api.moguding.net:9000/attendence/clock/v2/save"
    res = requests.post(url=url, headers=headers2, data=json.dumps(data))
    return res.json()["code"] == 200, res.json()["msg"]

def testNetword():
    url = "https://api.moguding.net:9000"
    try:
        ip = requests.get("http://4.ipw.cn").text
        requests.get(url,timeout=8)
    except Exception as e:
        e.with_traceback()
        return False,{"code": "400", "msg": "网络错误",'ip':ip}
    return True,{"code": "200", "msg": "网络正常",'ip':ip}