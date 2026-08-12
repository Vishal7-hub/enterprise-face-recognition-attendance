from datetime import date, time

from pydantic import BaseModel


class AttendanceResponse(BaseModel):
    id: int
    employee_id: int
    attendance_date: date
    attendance_time: time

    model_config = {
        "from_attributes": True
    }