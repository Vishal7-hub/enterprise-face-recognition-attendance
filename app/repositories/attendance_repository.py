from datetime import date

from sqlalchemy.orm import Session

from app.models.attendance import Attendance


def find_today_attendance(
    db: Session,
    employee_id: int,
):
    return (
        db.query(Attendance)
        .filter(
            Attendance.employee_id == employee_id,
            Attendance.attendance_date == date.today(),
        )
        .first()
    )


def create_attendance(
    db: Session,
    employee_id: int,
):
    from datetime import datetime

    now = datetime.now()

    attendance = Attendance(
        employee_id=employee_id,
        attendance_date=now.date(),
        attendance_time=now.time(),
    )

    db.add(attendance)
    db.commit()
    db.refresh(attendance)

    return attendance