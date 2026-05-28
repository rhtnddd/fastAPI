# web/student.py
# 역할: 5계층 (Controller) - HTTP 요청/응답 및 라우팅 전담

from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from ch09.db_connect import get_db
from ch09.schema.student import StudentCreate, StudentUpdate, StudentResponse
from ch09.service import student as student_service

router = APIRouter(prefix="/students", tags=["Students"])


# ── 1. 학생 추가 ──────────────────────────────────────────────────────
@router.post(
    "/",
    response_model=StudentResponse,
    status_code=status.HTTP_201_CREATED,
    summary="학생 추가"
)
def create_student(data: StudentCreate, db: Session = Depends(get_db)):
    """
    클라이언트로부터 이름, 성별, 소속학과 ID, 지망학과 ID를 받아 DB에 저장합니다.
    """
    return student_service.add_student(db, data)


# ── 2. 학생 수정 ──────────────────────────────────────────────────────
@router.patch(
    "/{student_id}",
    response_model=StudentResponse,
    summary="학생 정보 수정"
)
def update_student(student_id: int, data: StudentUpdate, db: Session = Depends(get_db)):
    """
    특정 학생의 이름(또는 기타 정보)을 변경합니다.
    데이터가 없으면 404 에러를 반환합니다.
    """
    return student_service.modify_student(db, student_id, data)


# ── 3. 학생 삭제 ──────────────────────────────────────────────────────
@router.delete(
    "/{student_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="학생 삭제"
)
def delete_student(student_id: int, db: Session = Depends(get_db)):
    """
    특정 학생을 DB에서 삭제합니다.
    데이터가 없으면 404 에러를 반환합니다.
    """
    student_service.remove_student(db, student_id)


# ── 4. 학과별 소속 학생 조회 ─────────────────────────────────────────
@router.get(
    "/department/{dept_id}/students",
    response_model=list[StudentResponse],
    summary="학과별 소속 학생 조회"
)
def get_students_by_department(dept_id: int, db: Session = Depends(get_db)):
    """
    특정 학과(dept_id)에 소속된 모든 학생 목록을 반환합니다.
    """
    return student_service.get_students_by_dept(db, dept_id)


# ── 5. 학과별 지망 학생 조회 ─────────────────────────────────────────
@router.get(
    "/department/{dept_id}/preferred-students",
    response_model=list[StudentResponse],
    summary="학과별 지망 학생 조회"
)
def get_preferred_students(dept_id: int, db: Session = Depends(get_db)):
    """
    특정 학과를 지망하는 모든 학생 목록을 반환합니다.
    """
    return student_service.get_preferred_students_by_dept(db, dept_id)