from datetime import date

from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.schemas.attendance import AttendanceResponse
from app.services.attendance_service import (
    mark_attendance,
    get_employee_attendance_history,
    get_date_attendance,
)


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


@router.get(
    "/employee/{employee_id}",
    response_model=list[AttendanceResponse],
)
def employee_attendance_history(
    employee_id: int,
    db: Session = Depends(get_db),
):
    return get_employee_attendance_history(
        db=db,
        employee_id=employee_id,
    )


@router.get(
    "/date/{attendance_date}",
    response_model=list[AttendanceResponse],
)
def attendance_by_date(
    attendance_date: date,
    db: Session = Depends(get_db),
):
    return get_date_attendance(
        db=db,
        attendance_date=attendance_date,
    )