from sqlalchemy.orm import Session

from app.models.employee import Employee
from app.schemas.employee import EmployeeCreate


def create_employee(
    db: Session,
    employee: EmployeeCreate,
):
    db_employee = Employee(
        employee_code=employee.employee_code,
        name=employee.name,
        department=employee.department,
        email=employee.email,
    )

    db.add(db_employee)

    db.commit()

    db.refresh(db_employee)

    return db_employee


def find_by_employee_code(
    db: Session,
    employee_code: str,
):
    return (
        db.query(Employee)
        .filter(Employee.employee_code == employee_code)
        .first()
    )


def find_by_employee_id(
    db: Session,
    employee_id: int,
):
    return (
        db.query(Employee)
        .filter(Employee.id == employee_id)
        .first()
    )


def update_employee_image_path(
    db: Session,
    employee: Employee,
    image_path: str,
):
    employee.profile_image_path = image_path

    db.commit()

    db.refresh(employee)

    return employee