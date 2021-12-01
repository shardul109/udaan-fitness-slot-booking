from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from loguru import logger
from uvicorn import run

from src.db.models import init_db
from src.router.functionality import router as functionality_router
from src.router.masters_router import router as masters_router

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
    expose_headers=["*"]
)

app.include_router(masters_router)
app.include_router(functionality_router)


@app.on_event('startup')
async def init_process():
    init_db()
    logger.info('server started')


if __name__ == '__main__':
    run("main:app", host="127.0.0.1", port=5002, reload=True)
