from sqlalchemy.orm import Session
from fastapi import HTTPException


from app.repositories.employee_repository import create_employee
from app.schemas.employee import EmployeeCreate
from app.repositories.employee_repository import (
    create_employee,
    find_by_employee_code,
)

def register_employee(db:Session , employee: EmployeeCreate,):

    existing_employee = find_by_employee_code(
        db=db,
        employee_code=employee.employee_code,
    )

    if existing_employee:
        raise HTTPException(
            status_code =409,
            detail = "Employee code already exists",
        )

    return create_employee(
    db=db,
    employee=employee,
    )
    




    
