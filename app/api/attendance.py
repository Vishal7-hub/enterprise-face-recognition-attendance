from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.schemas.attendance import AttendanceResponse
from app.services.attendance_service import mark_attendance


router = APIRouter(
    prefix="/attendance",
    tags=["Attendance"],
)


@router.post(
    "/mark/{employee_id}",
    response_model=AttendanceResponse,
    status_code=status.HTTP_201_CREATED,
)
def mark_employee_attendance(
    employee_id: int,
    db: Session = Depends(get_db),
):
    return mark_attendance(
        db=db,
        employee_id=employee_id,
    )
    