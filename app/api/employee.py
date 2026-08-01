from fastapi import APIRouter, Depends, status, UploadFile, File
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.services.employee_service import (
    register_employee,
    upload_employee_image,
)
from app.schemas.employee import (
    EmployeeCreate,
    EmployeeResponse,
)

router = APIRouter(
    prefix="/employees",
    tags=["Employees"],
)


@router.post("/{employee_code}/image")
def upload_employee_image_api(
    employee_code: str,
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
):
    return upload_employee_image(
        db=db,
        employee_code=employee_code,
        file=file,
    )


@router.post(
    "",
    response_model=EmployeeResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_employee(
    employee: EmployeeCreate,
    db: Session = Depends(get_db),
):
    return register_employee(
        db=db,
        employee=employee,
    )