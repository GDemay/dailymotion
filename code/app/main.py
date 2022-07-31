import logging
from typing import List

from app.api.api_v1.api import api_router
from app.db.session import SessionLocal
from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware
from app.core.config import settings

app = FastAPI(debug=True)

logger = logging.getLogger("")
logging.basicConfig(level=logging.DEBUG)


app.include_router(api_router, prefix=settings.API_VERSION)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
def hello_world():
    return {"msg": "Hello World"}
