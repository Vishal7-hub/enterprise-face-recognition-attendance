from fastapi import FastAPI

from app.core.config import settings
from app.core.logger import logger
import app.models
from app.db.session import Base,engine

app = FastAPI(
    title=settings.APP_NAME,
    version=settings.APP_VERSION,
    description="Production-ready facial recognition attendance system.",
)


@app.on_event("startup")
async def startup():
    Base.metadata.create_all(bind=engine)
    logger.info("Application Started Successfully")


@app.get("/")
async def root():
    return {
        "message": settings.APP_NAME,
        "version": settings.APP_VERSION,
    }


@app.get("/health")
async def health():
    return {
        "status": "healthy"
        
    }