from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from ch09.db_connect import Base
from ch09.model.student import Student

class Department(Base):
    __tablename__ = 'department'
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, nullable=False, unique=True)
    personnel = Column(Integer, nullable=False)
    # 파이썬 객체에서만 존재하는 가상 속성
    students = relationship(
        "Student",
        back_populates="department",
        foreign_keys="Student.department_id"
    )
    preferred_students = relationship(
        "Student",
        back_populates="preferred_department",
        foreign_keys="Student.preferred_department_id"
    )