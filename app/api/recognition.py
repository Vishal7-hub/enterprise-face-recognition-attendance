import shutil
from pathlib import Path

from fastapi import APIRouter, Depends, File, UploadFile
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.services.recognition_service import recognize_face


router = APIRouter(
    prefix="/recognition",
    tags=["Recognition"],
)


@router.post("/verify")
def verify_face(
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
):
    temp_path = Path("uploads") / "recognition_temp.jpg"

    with open(temp_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    result = recognize_face(
        db=db,
        image_path=str(temp_path),
    )

    if result is None:
        return {
            "recognized": False,
            "message": "Face not recognized",
        }

    return {
        "recognized": True,
        "employee_id": result["employee_id"],
        "similarity": result["similarity"],
    }