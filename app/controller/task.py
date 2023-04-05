from app import app
from app.model.config import Config
from app.common import gxyUtils
from fastapi_jwt import JwtAuthorizationCredentials
from fastapi import Security, HTTPException
from app.common.jwt import access_security

@app.get("/api/sign/status")
def SignStatus(credentials: JwtAuthorizationCredentials = Security(access_security)):
    if credentials is None:
        return {"code": 400, "msg": "用户未登录"}
    currentUser: Config = Config.get_or_none(Config.userId == credentials["userId"])
    if currentUser is None:
        return {"code": 400, "msg": "用户不存在"}
    try:
        logs = gxyUtils.getSignLogs(currentUser.userId)
    except:
        return {"code": 400, "msg": "获取签到状态失败"}
    return {"code": 200, "msg": "ok", "data": logs}