import uvicorn
from app import app

if __name__ == "__main__":
    from app.model import config
    # config.test()
    uvicorn.run(app, host="0.0.0.0", port=8000)