# model/todo.py
from pydantic import BaseModel
from datetime import datetime

class Todo(BaseModel):
    """할 일 입력용 데이터 모델"""
    task: str

class TodoResponse(Todo):
    """할 일 응답용 데이터 모델 (DB 저장 후 반환)"""
    todo_id: int
    completed: bool = False  # DB의 INTEGER 0/1이 Python의 bool False/True로 변환
    created_at: datetime