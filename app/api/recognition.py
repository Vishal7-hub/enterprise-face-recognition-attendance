import shutil
from pathlib import Path

from fastapi import APIRouter, Depends, File, UploadFile, HTTPException
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.services.recognition_service import recognize_face
from app.services.attendance_service import mark_attendance


router = APIRouter(
    prefix="/recognition",
    tags=["Recognition"],
)


# --------------------------------------------------
# Manual Face Verification
# --------------------------------------------------

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


# --------------------------------------------------
# Live Camera Recognition + Attendance
# --------------------------------------------------

@router.post("/camera")
async def recognize_from_camera(
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
):
    temp_path = Path("uploads") / "camera_frame.jpg"

    with open(temp_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    # Recognize face
    result = recognize_face(
        db=db,
        image_path=str(temp_path),
    )

    # No employee recognized
    if result is None:
        return {
            "recognized": False,
            "message": "Face not recognized",
        }

    employee_id = result["employee_id"]

    # Automatically mark attendance
    try:

        mark_attendance(
            db=db,
            employee_id=employee_id,
        )

        attendance_status = "Attendance marked"

    except HTTPException as e:

        if e.status_code == 409:
            attendance_status = "Attendance already marked today"
        else:
            raise

    return {
        "recognized": True,
        "employee_id": employee_id,
        "similarity": result["similarity"],
        "attendance": attendance_status,
    }