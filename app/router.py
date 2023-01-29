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
from fastapi import FastAPI, Query
from pydantic import BaseModel, Field
import json
from app.model.config import Config,create_or_update as createConfig

@app.get("/")
async def get_index():
    return FileResponse('web/index.html')


# @app.get("/{whatever:path}")
# async def get_static_files_or_404(whatever):
#     # try open file for path
#     file_path = os.path.join("web", whatever)
#     if os.path.isfile(file_path):
#         return FileResponse(file_path)
#     return {"code": "404"}


@app.get("/user/{phone}")
def read_item(phone: int):
    return db.getOneByPhone(phone)


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
    
    return {"access_token": access_security.create_access_token(subject=data)}

@app.get("/api/config")
def getConfig(phone: Union[str, None] = Query(None, regex="^\d{11}$")):
    config = Config.get_or_none(Config.phone == phone)
    if config is None:
        return {"code": "400", "msg": "用户不存在"}
    return config.get().__data__