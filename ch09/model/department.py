# model/department.py
# 역할: 1계층 (Entity) - DB 테이블 설계

from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from ch09.db_connect import Base


class Department(Base):
    __tablename__ = "departments"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    name = Column(String(100), nullable=False, unique=True)
    personnel = Column(Integer, nullable=False, default=0)

    # 역참조: 소속 학생 목록
    students = relationship("Student", foreign_keys="Student.department_id", back_populates="department")

    def __repr__(self):
        return f"<Department(id={self.id}, name={self.name}, personnel={self.personnel})>"