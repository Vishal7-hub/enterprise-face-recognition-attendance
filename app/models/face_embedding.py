from datetime import datetime
from sqlalchemy import Column, DateTime, ForeignKey, Integer, LargeBinary, String
from sqlalchemy import Column, DateTime, ForeignKey, Integer, LargeBinary

from app.db.session import Base


class FaceEmbedding(Base):
    __tablename__ = "face_embeddings"

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

    embedding = Column(
        LargeBinary,
        nullable=False,
    )

    model_name = Column(
        String(50),
        nullable=False,
    )

    created_at = Column(
        DateTime,
        default=datetime.utcnow,
        nullable=False,
    )