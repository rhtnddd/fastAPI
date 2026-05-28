# model/student.py
# 역할: 1계층 (Entity) - DB 테이블 설계

import enum
from sqlalchemy import Column, Integer, String, Enum, ForeignKey
from sqlalchemy.orm import relationship
from ch09.db_connect import Base


class Gender(enum.Enum):
    MALE = "MALE"
    FEMALE = "FEMALE"


class Student(Base):
    __tablename__ = "students"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    name = Column(String(50), nullable=False)
    gender = Column(Enum(Gender), nullable=False)

    # 소속 학과 (실제 학과)
    department_id = Column(Integer, ForeignKey("departments.id"), nullable=True)
    department = relationship("Department", foreign_keys=[department_id], back_populates="students")

    # 지망 학과
    preferred_department_id = Column(Integer, ForeignKey("departments.id"), nullable=True)
    preferred_department = relationship("Department", foreign_keys=[preferred_department_id])

    def __repr__(self):
        return f"<Student(id={self.id}, name={self.name}, gender={self.gender})>"