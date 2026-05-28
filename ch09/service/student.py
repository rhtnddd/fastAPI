# service/student.py
# 역할: 4계층 (Business) - 비즈니스 로직 및 예외 처리 전달

from sqlalchemy.orm import Session
from fastapi import HTTPException, status

from ch09.data import student as student_repo
from ch09.schema.student import StudentCreate, StudentUpdate
from ch09.model.student import Student


def _get_or_404(db: Session, student_id: int) -> Student:
    """공통 헬퍼: 학생이 없으면 404 예외 발생"""
    student = student_repo.get_student_by_id(db, student_id)
    if not student:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"학생 ID {student_id}을(를) 찾을 수 없습니다."
        )
    return student


def add_student(db: Session, data: StudentCreate) -> Student:
    """학생 추가"""
    return student_repo.create_student(db, data)


def modify_student(db: Session, student_id: int, data: StudentUpdate) -> Student:
    """학생 이름(및 기타 정보) 수정 - 존재하지 않으면 404"""
    student = _get_or_404(db, student_id)
    return student_repo.update_student(db, student, data)


def remove_student(db: Session, student_id: int) -> None:
    """학생 삭제 - 존재하지 않으면 404"""
    student = _get_or_404(db, student_id)
    student_repo.delete_student(db, student)


def get_students_by_dept(db: Session, department_id: int) -> list[Student]:
    """학과별 소속 학생 목록 반환"""
    return student_repo.get_students_by_department(db, department_id)


def get_preferred_students_by_dept(db: Session, department_id: int) -> list[Student]:
    """학과를 지망하는 학생 목록 반환"""
    return student_repo.get_students_by_preferred_department(db, department_id)