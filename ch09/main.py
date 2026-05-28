# main.py
# 역할: 진입점 - FastAPI 앱 및 라우터 등록

from fastapi import FastAPI
from ch09.db_connect import Base, engine

# 모델을 import해야 Base.metadata에 테이블 정보가 등록됩니다
from ch09.model import department, student  # noqa: F401 (side-effect import)
from ch09.web import student as student_router

# ── 테이블 자동 생성 ─────────────────────────────────────────────────
Base.metadata.create_all(bind=engine)

# ── FastAPI 앱 생성 ──────────────────────────────────────────────────
app = FastAPI(
    title="학생 관리 API",
    description="FastAPI + SQLAlchemy 5계층 구조 실습",
    version="1.0.0",
)

# ── 라우터 등록 ──────────────────────────────────────────────────────
app.include_router(student_router.router)


@app.get("/", tags=["Health"])
def root():
    return {"message": "학생 관리 API 서버가 정상 동작 중입니다."}