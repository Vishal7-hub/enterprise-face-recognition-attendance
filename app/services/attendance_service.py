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
