from datetime import datetime
from sqlalchemy import Boolean,Column,DateTime,Integer,String




from app.db.session import Base

class Employee(Base):
    __tablename__ = "employees"
    id = Column(
    Integer,
    primary_key=True,
    )

    employee_code = Column(
    String(20),
    unique=True,
    nullable=False,
    index=True
    )


    name = Column(
    String(100),
    nullable=False,
    )

     

    department = Column(
    String(50),
    nullable=False,
    )


    email = Column(
    String(255),
    nullable=True,
    )


    profile_image_path = Column(
    String(255),
    nullable=True,
    )

    is_active = Column(
    Boolean,
    default=True,
    nullable=False,
    )

    created_at = Column(
    DateTime,
    default=datetime.utcnow,
    nullable=False,
    )


    



    





