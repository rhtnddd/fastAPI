# Step 3. 데이터베이스 창고지기 (data/todo.py)
# ✅ 중복 문제를 막기 위해 모두 **고유번호(todo_id)**를 기반으로 처리하도록 업그레이드
# data/todo.py
import os
from sqlite3 import IntegrityError, connect
from typing import List, Generator
from error import Duplicate, Missing
from model.todo import TodoResponse, Todo

class DBConnect:
    def __init__(self, db_name='todo.db', check_same_thread=True):
        self.conn = connect(db_name, check_same_thread=check_same_thread)
        # SQLite3는 기본적으로 dict_factory를 지원하지 않으므로 직접 구현합니다.
        self.conn.row_factory = self._dict_factory
        self.cursor = self.conn.cursor()
        # 테이블 생성 로직을 DBConnect 생성자로 이동
        self.cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS todos (
                todo_id INTEGER PRIMARY KEY AUTOINCREMENT,
                task TEXT NOT NULL UNIQUE,
                completed INTEGER NOT NULL DEFAULT 0,
                created_at TEXT NOT NULL DEFAULT (datetime('now', 'localtime'))
            )
            """
        )
        self.conn.commit()

    def _dict_factory(self, cursor, row):
        # 딕셔너리 형태로 결과를 반환하기 위한 헬퍼 함수
        d = {}
        for idx, col in enumerate(cursor.description):
            d[col[0]] = row[idx]
        return d

    def get_cursor(self):
        return self.cursor

    def commit(self):
        self.conn.commit()

    def close(self):
        self.conn.close()

# FastAPI 의존성 주입을 위한 DB 연결 함수
def get_db() -> Generator[DBConnect, None, None]:
    # Uvicorn 워커 스레드에서 접근 가능하도록 check_same_thread=False 설정
    db_instance = DBConnect(check_same_thread=False)
    try:
        yield db_instance
    finally:
        db_instance.close()

# 모든 함수가 db: DBConnect 인자를 받도록 수정
def find_all(db: DBConnect) -> List[TodoResponse]:
    db.get_cursor().execute("select * from todos")
    return [TodoResponse(**dict(row)) for row in db.get_cursor().fetchall()]

def insert_one(db: DBConnect, todo: Todo) -> TodoResponse:
    query = "insert into todos(task) values(:task)"
    param = todo.model_dump()
    try:
        db.get_cursor().execute(query, param)
        db.commit() # db 객체의 commit 메서드 사용
    except IntegrityError as e:
        print(e)
        raise Duplicate(msg=f"'{todo.task}'은(는) 이미 존재합니다.")

    todo_id = db.get_cursor().lastrowid
    db.get_cursor().execute(f"SELECT * FROM todos WHERE todo_id = {todo_id}")
    return TodoResponse(**dict(db.get_cursor().fetchone()))

def get_one(db: DBConnect, todo_id: int) -> TodoResponse:
    db.get_cursor().execute("SELECT * FROM todos WHERE todo_id = ?", (todo_id,))
    row = db.get_cursor().fetchone()
    if row:
        return TodoResponse(**dict(row))
    else:
        raise Missing(msg=f"ID {todo_id} 항목을 찾을 수 없습니다.")

def modify_completed(db: DBConnect, todo_id: int) -> TodoResponse:
    query = "update todos set completed = not completed where todo_id = ?"
    db.get_cursor().execute(query, (todo_id,))
    db.commit() # db 객체의 commit 메서드 사용
    if db.get_cursor().rowcount == 1:
        return get_one(db, todo_id) # 수정된 get_one 호출 시 db 인자 전달
    else:
        raise Missing(msg=f"ID {todo_id} 항목을 찾을 수 없습니다.")

def delete(db: DBConnect, todo_id: int) -> bool:
    query = "delete from todos where todo_id = ?"
    db.get_cursor().execute(query, (todo_id,))
    db.commit() # db 객체의 commit 메서드 사용
    if db.get_cursor().rowcount != 1:
        raise Missing(msg=f"ID {todo_id} 항목을 찾을 수 없습니다.")
    return True