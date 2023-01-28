from app import app
from starlette.responses import FileResponse
import db
import os

from app import jwt

@app.get("/")
async def get_index():
    return FileResponse('web/index.html')

@app.get("/{whatever:path}")
async def get_static_files_or_404(whatever):
    # try open file for path
    file_path = os.path.join("web",whatever)
    if os.path.isfile(file_path):
        return FileResponse(file_path)
    return {"code": "404"}

@app.get("/h")
def read_root():
    return {"Hello": "World"}


@app.get("/user/{phone}")
def read_item(phone: int):
    return db.getOneByPhone(phone)
