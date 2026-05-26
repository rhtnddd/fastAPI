# Step 5. API 라우터 (web/todo.py)
# 클라이언트(브라우저)의 요청을 받아 서비스(주방장)에게 넘기고, 에러가 발생하면 HTTP 예외 처리(404 등)를 던집니다.
# web/todo.py
from typing import List
from fastapi import APIRouter, HTTPException, Depends # Depends 임포트
from error import Duplicate, Missing
from model.todo import TodoResponse, Todo
import service.todo as service
from data.todo import DBConnect, get_db # DBConnect와 get_db 임포트

router = APIRouter(prefix="/todo")

@router.get('')
def get_all(db: DBConnect = Depends(get_db)) -> List[TodoResponse]: # DB 의존성 주입
    return service.find_all(db)

@router.post('')
def insert_one(todo: Todo, db: DBConnect = Depends(get_db)) -> TodoResponse: # DB 의존성 주입
    try:
        return service.insert_one(db, todo)
    except Duplicate as e:
        raise HTTPException(status_code=400, detail=e.msg)

@router.get('/{todo_id}')
def get_one(todo_id: int, db: DBConnect = Depends(get_db)) -> TodoResponse: # DB 의존성 주입
    try:
        return service.get_one(db, todo_id)
    except Missing as e:
        raise HTTPException(status_code=404, detail=e.msg)

@router.patch('/{todo_id}')
def modify_completed(todo_id: int, db: DBConnect = Depends(get_db)) -> TodoResponse: # DB 의존성 주입
    try:
        return service.modify_completed(db, todo_id)
    except Missing as e:
        raise HTTPException(status_code=404, detail=e.msg)

@router.delete("/{todo_id}")
def delete(todo_id: int, db: DBConnect = Depends(get_db)) -> bool: # DB 의존성 주입
    try:
        return service.delete(db, todo_id)
    except Missing as exc:
        raise HTTPException(status_code=404, detail=exc.msg)