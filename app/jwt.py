from fastapi import FastAPI, Security, HTTPException
from fastapi_jwt import JwtAuthorizationCredentials, JwtAccessBearer
from app import app

access_security = JwtAccessBearer(secret_key="this_is_miyao", auto_error=False)

@app.post("/auth")
def auth():
    subject = {"username": "username", "role": "user"}
    return {"access_token": access_security.create_access_token(subject=subject)}


@app.get("/users/me")
def read_current_user(
    credentials: JwtAuthorizationCredentials = Security(access_security),
):
    if not credentials:
        raise HTTPException(status_code=401, detail='Unauthorized')
    return {"username": credentials["username"], "role": credentials["role"]}
