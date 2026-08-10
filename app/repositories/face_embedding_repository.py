from sqlalchemy.orm import Session

from app.models.face_embedding import FaceEmbedding


def create_face_embedding(
    db: Session,
    employee_id: int,
    embedding: bytes,
    model_name: str,
):
    db_embedding = FaceEmbedding(
        employee_id=employee_id,
        embedding=embedding,
        model_name=model_name,
    )

    db.add(db_embedding)
    db.commit()
    db.refresh(db_embedding)

    return db_embedding


def get_embeddings_by_employee(
    db: Session,
    employee_id: int,
):
    return (
        db.query(FaceEmbedding)
        .filter(FaceEmbedding.employee_id == employee_id)
        .all()
    )


def get_all_face_embeddings(db: Session):
    return db.query(FaceEmbedding).all()