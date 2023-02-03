from app import app
from starlette.responses import FileResponse
import db
import os
from app.common.jwt import access_security
from app.common.captcha import getCode
import uuid
import requests
from app.common.utils import encrypt
import time
from typing import Union
from fastapi import FastAPI, Query,Security,HTTPException
from pydantic import BaseModel, Field
import json
from app.model.config import Config,create_or_update as createConfig
from fastapi_jwt import JwtAuthorizationCredentials, JwtAccessBearer
from app.common.utils import getSign

@app.get("/")
async def get_index():
    return FileResponse('web/dist/index.html')


# @app.get("/{whatever:path}")
# async def get_static_files_or_404(whatever):
#     # try open file for path
#     file_path = os.path.join("web/dist", whatever)
#     if os.path.isfile(file_path):
#         return FileResponse(file_path)
#     return FileResponse('web/dist/index.html')



class UserInfo(BaseModel):
    phone: Union[str, None] = Field(default=None, regex="^\d{11}$")
    password: Union[str, None] = Field(
        default=None, min_length=6, max_length=20)


@app.post("/api/login")
def login(user: UserInfo):
    """实现登录接口"""
    if user.phone is None or user.password is None:
        return {"code": "400", "msg": "参数错误"}
    uuidStr = str(uuid.uuid4())
    # 获取一个验证码
    captcha = getCode(uuidStr)
    while len(captcha) != 5:
        captcha = getCode(uuidStr)
    headers = {
        "roleKey": "student",
        "host": "api.moguding.net:9000",
        "origin": "https://api.moguding.net",
        "referer": "https://api.moguding.net/",
        "content-type": "application/json; charset=UTF-8",
    }
    datas = {"t": encrypt(str(int(time.time() * 1000))),
             "phone": encrypt(user.phone),
             "password": encrypt(user.password),
             "captcha": captcha,
             "loginType": "web",
             "uuid": uuidStr
             }
    res = requests.post('https://api.moguding.net:9000/session/user/v3/login',
                        headers=headers,data=json.dumps(datas),verify=False)
    data = res.json()
    if data["code"] != 200:
        return data
    data = data["data"]
    createConfig(user.phone, user.password, data["token"], data["userId"])
    
    return {"code":200,"msg":"登录成功","token": access_security.create_access_token(subject=data)}

@app.get("/api/config")
def getConfig(currentUser: JwtAuthorizationCredentials = Security(access_security)):
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
    phone: Union[str, None] = Field(default=None, regex="^\d{11}$")
    password: Union[str, None] = Field(
        default=None, min_length=6, max_length=20)
    planId: Union[str, None] = Field(default=None)
    userAgent: Union[str, None] = Field(default=None)
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
def setConfig(newconfig: UserConfig,currentUser: JwtAuthorizationCredentials = Security(access_security)):
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
def getPlan(currentUser: JwtAuthorizationCredentials = Security(access_security)):
    url = "https://api.moguding.net:9000/practice/plan/v3/getPlanByStu"
    data = {
        "state": 1,
        "t": encrypt(str(int(time.time() * 1000)))
    }
    headers2 = {
        'roleKey': 'student',
        "authorization": currentUser["token"],
        "sign": getSign(currentUser["userId"]),
        "content-type": "application/json; charset=UTF-8",
    }
    res = requests.post(url=url, data=json.dumps(data), headers=headers2)
    return res.json()
    

@app.get("/api/login")
def getConfig(credentials: JwtAuthorizationCredentials = Security(access_security)):
    if not credentials:
        raise HTTPException(status_code=401, detail='Unauthorized')
    return {"code":200,"userId": credentials["userId"]}