"""Thin API layer to handle I/O and exceptions"""
import logging

from fastapi import FastAPI, HTTPException
from validators.url import url  # type: ignore

from src.processing import process_url

log = logging.getLogger(__name__)

app = FastAPI()


@app.get("/health")
async def read_health():
    """health check endpoint"""
    return {"msg": "OK"}


@app.get("/urls")
async def read_urls(url: str):
    """returns word count for specified url"""
    if not is_url_valid(url):
        raise HTTPException(status_code=422, detail="The provided input does not appear to be a valid url")

    try:
        result = process_url(url)
        return {"data": result}

    except Exception as e:
        log.exception(e)
        raise HTTPException(status_code=500, detail="Internal error")


def is_url_valid(url_string: str) -> bool:
    """uses validators to determine whether a string is a valid url"""
    return url(url_string)
