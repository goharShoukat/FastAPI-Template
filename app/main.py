from fastapi import FastAPI

from app.core.lifespan_ import lifespan

app = FastAPI(lifespan=lifespan)
# app.include_router(router)
