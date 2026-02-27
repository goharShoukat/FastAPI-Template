from fastapi import FastAPI
from .core.lifespan_ import lifespan

app = FastAPI(lifespan=lifespan)


@app.get("/health")
async def health_check():
    return {"status": "healthy"}
