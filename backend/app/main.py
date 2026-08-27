from fastapi import FastAPI
from app.core.config import config
from app.api.v1 import health

app = FastAPI(title=config.app_name)

app.include_router(router=health.router, prefix="/v1")
