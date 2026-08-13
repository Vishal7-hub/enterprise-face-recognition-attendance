from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.repositories.attendance_repository import (
    create_attendance,
    find_today_attendance,
)


def mark_attendance(
    db: Session,
    employee_id: int,
):
    existing = find_today_attendance(
        db=db,
        employee_id=employee_id,
    )

    if existing:
        raise HTTPException(
            status_code=409,
            detail="Attendance already marked for today",
        )

    return create_attendance(
        db=db,
        employee_id=employee_id,
    )


from datetime import date

from app.repositories.attendance_repository import (
    get_employee_attendance,
    get_attendance_by_date,
)


def get_employee_attendance_history(
    db: Session,
    employee_id: int,
):
    return get_employee_attendance(
        db=db,
        employee_id=employee_id,
    )


def get_date_attendance(
    db: Session,
    attendance_date: date,
):
    return get_attendance_by_date(
        db=db,
        attendance_date=attendance_date,
    )
