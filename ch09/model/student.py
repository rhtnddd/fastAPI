import enum
from sqlalchemy import Column, Integer, String, Float, ForeignKey, Enum
from sqlalchemy.orm import relationship
from ch09.db_connect import Base

class Gender(enum.Enum):
    MALE = "MALE"
    FEMALE = "FEMALE"

class Student(Base):
    __tablename__ = "student"
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, nullable=False)
    gender = Column(Enum(Gender), nullable=False)
    score = Column(Float, default=0.0)
    department_id = Column(Integer, ForeignKey('department.id'), nullable=False)
    preferred_department_id = Column(Integer, ForeignKey('department.id'), nullable=True)
    # 파이썬 객체에서만 존재하는 가상 속성
    department = relationship(
        "Department",
        back_populates="students",
        foreign_keys=[department_id]
    )

    preferred_department = relationship(
        "Department",
        back_populates="preferred_students",
        foreign_keys=[preferred_department_id]
    )