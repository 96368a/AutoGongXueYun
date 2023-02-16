from app import app
from starlette.responses import FileResponse
import requests

from app.common.gxyUtils import testNetword

@app.get("/")
async def get_index():
    return FileResponse('web/dist/index.html')

@app.get("/api/test")
async def testApi():
    res,data=testNetword()
    return data