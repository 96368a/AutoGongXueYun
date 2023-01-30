from fastapi import FastAPI, Security, HTTPException
from fastapi_jwt import JwtAuthorizationCredentials, JwtAccessBearer
from app import app
from datetime import timedelta

try:
    import config
    jwt_key = config.jwtKey
except ImportError:
    jwt_key = "this_is_key"

access_security = JwtAccessBearer(secret_key=jwt_key, auto_error=False,access_expires_delta=timedelta(days=256))