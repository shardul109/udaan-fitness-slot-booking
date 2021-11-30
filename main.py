from typing import Optional
from loguru import logger
from fastapi import FastAPI
from uvicorn import run
from src.db.models import init_db
from src.router.masters_router import router as masters_router

app = FastAPI()
app.include_router(masters_router)


@app.on_event('startup')
async def init_process():
    init_db()
    logger.info('server started')


if __name__ == '__main__':
    run("main:app", host="127.0.0.1", port=5002, reload=True)
