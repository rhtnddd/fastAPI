from contextlib import asynccontextmanager
import uvicorn
from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
from ch09.db_connect import engine, Base, get_db
import ch09.model.department as department_model
import ch09.model.student as student_model


@asynccontextmanager
async def lifespan(app: FastAPI):
    # 내부적으로 "CREATE TABLE IF NOT EXISTS" 와 동일하게 동작
    Base.metadata.create_all(engine)
    print("[앱 시작] DB 테이블 생성")
    yield
    print("[앱 종료] 서버 종료")
app = FastAPI(lifespan=lifespan)
@app.get("/")
def index(db: Session = Depends(get_db)):
    dept = department_model.Department(name="공통학과", personnel=64)
    db.add(dept)
    db.commit()
    db.refresh(dept)
    print(dept.id)
    student = student_model.Student(name="ahn", gender=student_model.Gender.FEMALE, department_id=dept.id)
    db.add(student)
    db.commit()
    return {"message": "Department assignment system"}

if __name__ == '__main__':
    uvicorn.run("main:app", host='0.0.0.0', port=8000, reload=True)