from app import app
from starlette.responses import FileResponse


@app.get("/")
async def get_index():
    return FileResponse('web/dist/index.html')