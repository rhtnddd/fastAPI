from contextlib import contextmanager
from sqlalchemy import create_engine, Column, Integer, String  # create_engine 오타 수정
from sqlalchemy.orm import sessionmaker, declarative_base

# enginel -> engine으로 변수명 수정
engine = create_engine('sqlite:///test.db', connect_args={"check_same_thread": False})
Base = declarative_base()

class Department(Base):
    __tablename__ = 'department'
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False, unique=True)
    personnel = Column(Integer)

# 정상적으로 수정된 engine 변수 바인딩
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

@contextmanager
def get_db():
    db = SessionLocal()
    try:
        yield db
    except Exception as e:
        db.rollback()
        raise e
    finally:
        db.close()

if __name__ == '__main__':
    Base.metadata.create_all(bind=engine)
    with get_db() as db:
        dept = Department(name="SW개발과", personnel=32)
        db.add(dept)
        db.commit()