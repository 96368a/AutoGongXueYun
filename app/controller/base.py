from app import app
from starlette.responses import FileResponse
import requests

@app.get("/")
async def get_index():
    return FileResponse('web/dist/index.html')

@app.get("/api/test")
async def testApi():
    url = "https://api.moguding.net:9000"
    try:
        ip = requests.get("http://4.ipw.cn").text
        requests.get(url,timeout=8)
    except Exception as e:
        e.with_traceback()
        return {"code": "400", "msg": "网络错误",'ip':ip}
    return {"code": "200", "msg": "网络正常",'ip':ip}
    