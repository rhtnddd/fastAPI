# db_connect.py
# 역할: DB 엔진 및 세션 관리

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# SQLite 사용 (실제 환경에서는 MySQL, PostgreSQL 등으로 변경)
DATABASE_URL = "sqlite:///./ch08.db"

engine = create_engine(
    DATABASE_URL,
    connect_args={"check_same_thread": False}  # SQLite 전용 옵션
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


def get_db():
    """FastAPI Depends()에서 사용할 DB 세션 생성기"""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()