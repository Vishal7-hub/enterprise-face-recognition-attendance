from sqlalchemy.orm import Session
from fastapi import HTTPException
from pathlib import Path
from fastapi import HTTPException, UploadFile
import shutil
from app.core.config import settings
from app.repositories.employee_repository import (
    find_by_employee_code,
    update_employee_image_path,
)

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

import shutil
from pathlib import Path
from fastapi import HTTPException, UploadFile

def upload_employee_image(
    db,
    employee_code: str,
    file: UploadFile,
):
    employee = find_by_employee_code(
        db=db,
        employee_code=employee_code,
    )

    if not employee:
        raise HTTPException(
            status_code=404,
            detail="Employee not found",
        )

    image_path = Path(settings.UPLOAD_DIR) / f"{employee_code}.jpg"

    with open(image_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    return update_employee_image_path(
        db=db,
        employee=employee,
        image_path=str(image_path),
    )
    




    
