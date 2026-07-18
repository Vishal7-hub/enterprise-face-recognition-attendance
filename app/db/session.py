from sqlalchemy import create_engine

from sqlalchemy.orm import declarative_base

from sqlalchemy.orm import sessionmaker

from app.core.config import settings


engine = create_engine(
    settings.DATABASE_URL
    connect_args={"check_same_thread": False}
)

sessionLocal =sessionmaker(
    autocommit = False,
    autoflush = False,
    bind = engine

)

Base = declarative_base()

def get_db():
    db = sessionLocal()
    try:
        yield db
    finally:
        db.close()
         
