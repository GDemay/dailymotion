""" This is the main file of the application. """
import logging
from typing import List

from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware

from app.api.router import api_router
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
def hello_world() -> str:
    """_summary_: This is the main function of the application.

    Returns:
        _type_:  str - The string "Hello World"
    """
    return {"msg": "Hello World"}
