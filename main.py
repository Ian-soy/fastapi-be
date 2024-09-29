from fastapi import FastAPI

from components.db import init_db
from components.log import init_log, log
from components.env import init_env
from apis.gpts import gpts_router
from apis.ollama import ollama_router
from apis.test import test_router
from apis.audio import audio_router

# 示例化
app = FastAPI()
app.include_router(audio_router)
app.include_router(gpts_router)
app.include_router(ollama_router)
app.include_router(test_router)

@app.on_event("startup")
async def startup():
    """
    Startup function to initialize various components of the application.

    This function is responsible for initializing the logging system, environment variables,
    and the database connection. It ensures that all necessary components are set up
    before the application starts.

    Note:
    - This function is asynchronous and should be awaited when called.
    - The order of initialization is important, as subsequent operations may depend on
      the successful completion of previous steps.

    Returns:
        None
    """
    print("init log")
    init_log()
    print("init env")
    init_env()
    print("init db")
    init_db()

    log.info("app start")


@app.on_event("shutdown")
async def shutdown():
    log.info("app shutdown")