from datetime import datetime

from sqlalchemy import Column, Date, DateTime, ForeignKey, Integer, Time
from app.db.session import Base


class Attendance(Base):
    __tablename__ = "attendance"

    id = Column(
        Integer,
        primary_key=True,
    )

    employee_id = Column(
        Integer,
        ForeignKey("employees.id"),
        nullable=False,
        index=True,
    )

    attendance_date = Column(
        Date,
        nullable=False,
        index=True,
    )

    attendance_time = Column(
        Time,
        nullable=False,
    )

    created_at = Column(
        DateTime,
        default=datetime.utcnow,
        nullable=False,
    )