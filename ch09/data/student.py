# data/student.py
# 역할: 3계층 (Repository) - 순수 DB CRUD 조작 전담

from sqlalchemy.orm import Session
from ch09.model.student import Student
from ch09.schema.student import StudentCreate, StudentUpdate


def create_student(db: Session, data: StudentCreate) -> Student:
    """학생 레코드 INSERT"""
    student = Student(
        name=data.name,
        gender=data.gender,
        department_id=data.department_id,
        preferred_department_id=data.preferred_department_id,
    )
    db.add(student)
    db.commit()
    db.refresh(student)
    return student


def get_student_by_id(db: Session, student_id: int) -> Student | None:
    """PK로 학생 단건 조회"""
    return db.query(Student).filter(Student.id == student_id).first()


def get_students_by_department(db: Session, department_id: int) -> list[Student]:
    """소속 학과(department_id)로 학생 목록 조회"""
    return db.query(Student).filter(Student.department_id == department_id).all()


def get_students_by_preferred_department(db: Session, department_id: int) -> list[Student]:
    """지망 학과(preferred_department_id)로 학생 목록 조회"""
    return db.query(Student).filter(Student.preferred_department_id == department_id).all()


def update_student(db: Session, student: Student, data: StudentUpdate) -> Student:
    """학생 정보 UPDATE (변경된 필드만 반영)"""
    update_data = data.model_dump(exclude_unset=True)   # 전달된 필드만 추출
    for field, value in update_data.items():
        setattr(student, field, value)
    db.commit()
    db.refresh(student)
    return student


def delete_student(db: Session, student: Student) -> None:
    """학생 레코드 DELETE"""
    db.delete(student)
    db.commit()