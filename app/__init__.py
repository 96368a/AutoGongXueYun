from typing import Union
from fastapi import FastAPI


app = FastAPI()

# 初始化路由
from app import router