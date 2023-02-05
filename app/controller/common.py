from app import app
from typing import Union
import requests
from fastapi import FastAPI, Query
from fastapi_jwt import JwtAuthorizationCredentials
from fastapi import Security, HTTPException
from app.common.jwt import access_security


@app.get("/api/place/search")
def getPlace(location: Union[str, None] = Query(default=None, regex="^\d{1,3}\.\d{1,6},\d{1,3}\.\d{1,6}$"), credentials: JwtAuthorizationCredentials = Security(access_security)):
    if not credentials:
        raise HTTPException(status_code=401, detail='Unauthorized')
    try:
        from config import baiduMapKey
    except:
        return {"code": 400, "msg": "请先配置百度地图密钥"}
    url = f'https://api.map.baidu.com/place/v2/search?query=公司$汽车$餐饮$购物$生活$体育$医院$住宿$风景$学校&location={location}&radius=1000&output=json&ak={baiduMapKey}'
    res = requests.get(url)
    data = res.json()
    if data['status'] != 0:
        return {"code": 400, "msg": "请求失败"}
    return {"code": 200, "msg": "ok", "data": data['results']}
