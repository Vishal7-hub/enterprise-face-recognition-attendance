from fastapi import FastAPI
from pathlib import Path
from app.core.config import settings
from app.core.logger import logger
import app.models
from app.db.session import Base,engine
from app.api.employee import router as employee_router
from app.models.employee import Employee
from app.models.face_embedding import FaceEmbedding
app = FastAPI(
    title=settings.APP_NAME,
    version=settings.APP_VERSION,
    description="Production-ready facial recognition attendance system.",
)

Base.metadata.create_all(bind=engine)

app.include_router(employee_router)


@app.on_event("startup")
async def startup():

    Path(settings.UPLOAD_DIR).mkdir(
        parents=True,
        exist_ok=True,
    )

    logger.info("Upload folder ready")

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