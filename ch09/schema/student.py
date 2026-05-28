# schema/student.py
# 역할: 2계층 (DTO) - 클라이언트 입출력 데이터 검증

from pydantic import BaseModel
from typing import Optional
from ch09.model.student import Gender


# ── 요청(Request) 스키마 ──────────────────────────────────────────────

class StudentCreate(BaseModel):
    """POST /students - 학생 추가 요청 바디"""
    name: str
    gender: Gender
    department_id: Optional[int] = None
    preferred_department_id: Optional[int] = None


class StudentUpdate(BaseModel):
    """PATCH /students/{student_id} - 학생 수정 요청 바디"""
    name: Optional[str] = None
    gender: Optional[Gender] = None
    department_id: Optional[int] = None
    preferred_department_id: Optional[int] = None


# ── 응답(Response) 스키마 ─────────────────────────────────────────────

class StudentResponse(BaseModel):
    """클라이언트에게 반환할 학생 정보"""
    id: int
    name: str
    gender: Gender
    department_id: Optional[int] = None
    preferred_department_id: Optional[int] = None

    class Config:
        from_attributes = True   # SQLAlchemy 모델 → Pydantic 자동 변환 (구 orm_mode)