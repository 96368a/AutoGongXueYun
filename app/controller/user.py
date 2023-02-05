import requests
import time
import json
from typing import Union
from app import app
from app.common.loginUtils import loginCycle, refreshLogin
from app.common.jwt import access_security
from app.common.utils import encrypt, getSign
from app.model.config import Config
from fastapi_jwt import JwtAuthorizationCredentials
from fastapi import Security, HTTPException
from pydantic import BaseModel, Field


class UserInfo(BaseModel):
    phone: Union[str, None] = Field(default=None, regex="^\d{11}$")
    password: Union[str, None] = Field(
        default=None, min_length=6, max_length=20)


@app.post("/api/login")
def login(user: UserInfo):
    """实现登录接口"""
    if user.phone is None or user.password is None:
        return {"code": "400", "msg": "参数错误"}
    data = loginCycle(user.phone, user.password)
    if data["code"] == 200:
        return {"code": 200, "msg": "登录成功", "token": access_security.create_access_token(subject=data['data'])}
    return data


@app.get("/api/login")
def getConfig(credentials: JwtAuthorizationCredentials = Security(access_security)):
    """登录检查接口"""
    if not credentials:
        raise HTTPException(status_code=401, detail='Unauthorized')
    return {"code": 200, "userId": credentials["userId"]}


@app.get("/api/config")
def getConfig(currentUser: JwtAuthorizationCredentials = Security(access_security)):
    """获取用户配置"""
    if currentUser is None:
        raise HTTPException(status_code=401, detail='登录失效')
    userId = currentUser["userId"]
    config: Config = Config.get_or_none(Config.userId == userId)
    if config is None:
        return {"code": 400, "msg": "用户不存在"}
    user = config.get().__data__
    user['password'] = len(user['password']) * "*"
    user.pop("token")
    return user


class UserConfig(BaseModel):
    planId: Union[str, None] = Field(default=None)
    longitude: Union[str, None] = Field(default=None)
    latitude: Union[str, None] = Field(default=None)
    address: Union[str, None] = Field(default=None)
    desc: Union[str, None] = Field(default=None)
    type: Union[str, None] = Field(default=None)
    enable: Union[bool, None] = Field(default=None)
    keepLogin: Union[bool, None] = Field(default=None)
    randomLocation: Union[bool, None] = Field(default=None)
    plusplusKey: Union[str, None] = Field(default=None)
    ServerChanKey: Union[str, None] = Field(default=None)


@app.post("/api/config")
def setConfig(newconfig: UserConfig, currentUser: JwtAuthorizationCredentials = Security(access_security)):
    if currentUser is None:
        raise HTTPException(status_code=401, detail='登录失效')
    userId = currentUser["userId"]
    config: Config = Config.get_or_none(Config.userId == userId)
    if config is None:
        return {"code": 400, "msg": "用户不存在"}

    print(newconfig)

    user = config.get().__data__
    user['password'] = len(user['password']) * "*"
    user.pop("token")
    return user


@app.get("/api/plan")
def getPlan(credentials: JwtAuthorizationCredentials = Security(access_security)):
    currentUser = Config.get_or_none(Config.userId == credentials["userId"])
    if currentUser is None:
        return {"code": 400, "msg": "用户不存在"}
    currentUser = currentUser.get().__data__
    # 检查登录状态
    refreshLogin(currentUser["phone"])
    url = "https://api.moguding.net:9000/practice/plan/v3/getPlanByStu"
    data = {
        "state": 1,
        "t": encrypt(str(int(time.time() * 1000)))
    }
    headers2 = {
        'roleKey': 'student',
        "authorization": currentUser["token"],
        "sign": getSign(str(currentUser["userId"])),
        "content-type": "application/json; charset=UTF-8",
    }
    res = requests.post(url=url, data=json.dumps(data), headers=headers2)
    data = res.json()
    if data['code'] != 200:
        raise HTTPException(status_code=data['code'], detail=data['msg'])
    return data