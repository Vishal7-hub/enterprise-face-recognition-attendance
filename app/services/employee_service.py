from pathlib import Path
import shutil

import numpy as np
from fastapi import HTTPException, UploadFile
from sqlalchemy.orm import Session

from app.core.config import settings

from app.repositories.employee_repository import (
    create_employee,
    find_by_employee_code,
    update_employee_image_path,
)

from app.repositories.face_embedding_repository import (
    create_face_embedding,
)

from app.schemas.employee import EmployeeCreate

from app.services.face_service import generate_embedding


def register_employee(
    db: Session,
    employee: EmployeeCreate,
):
    existing_employee = find_by_employee_code(
        db=db,
        employee_code=employee.employee_code,
    )

    if existing_employee:
        raise HTTPException(
            status_code=409,
            detail="Employee code already exists",
        )

    return create_employee(
        db=db,
        employee=employee,
    )


def upload_employee_image(
    db: Session,
    employee_code: str,
    file: UploadFile,
):
    # 1. Find employee
    employee = find_by_employee_code(
        db=db,
        employee_code=employee_code,
    )

    if not employee:
        raise HTTPException(
            status_code=404,
            detail="Employee not found",
        )

    # 2. Create image path
    image_path = (
        Path(settings.UPLOAD_DIR)
        / f"{employee_code}.jpg"
    )

    # 3. Save uploaded image
    with open(image_path, "wb") as buffer:
        shutil.copyfileobj(
            file.file,
            buffer,
        )

    # 4. Generate face embedding
    embedding = generate_embedding(
        str(image_path)
    )

    # 5. Convert NumPy embedding to bytes
    embedding_bytes = (
        embedding
        .astype(np.float32)
        .tobytes()
    )

    # 6. Store embedding in database
    create_face_embedding(
        db=db,
        employee_id=employee.id,
        embedding=embedding_bytes,
        model_name="buffalo_l",
    )

    # 7. Store image path in employee record
    employee = update_employee_image_path(
        db=db,
        employee=employee,
        image_path=str(image_path),
    )

    return employee