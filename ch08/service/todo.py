# Step 4. 주서비스 계층 (service/todo.py)
# API와 데이터베이스 사이에서, AI 예측 모듈을 실행시켜 결과를 엮어내는 핵심 계층입니다.
# service/todo.py
import data.todo as data
from ml.predictor import predict_category
from model.todo import TodoResponse, Todo
from data.todo import DBConnect # DBConnect를 타입 힌트로 사용하기 위해 임포트

# 모든 함수가 db: DBConnect 인자를 받도록 수정
def find_all(db: DBConnect) -> list[TodoResponse]:
    return data.find_all(db)

def insert_one(db: DBConnect, todo: Todo) -> TodoResponse:
    # 🎯 [핵심] 할 일이 DB에 들어가기 전, AI에게 카테고리를 물어봅니다!
    ai_result = predict_category(todo.task)
    category= ai_result['predicted_category']
    score= ai_result['scores'][category]
    print(score)
    if score > 0.4:
        print(f"\n[AI 자동 분류 작동] '{todo.task}' -> 카테고리: {ai_result['predicted_category']}")

        return data.insert_one(db, todo)  # db 인자 전달
    else:
        print(f"\n[AI 자동 분류 작동] '{todo.task}' -> 카테고리: 기타")
        return data.insert_one(db, todo)

def get_one(db: DBConnect, todo_id: int) -> TodoResponse:
    return data.get_one(db, todo_id)

def modify_completed(db: DBConnect, todo_id: int) -> TodoResponse:
    return data.modify_completed(db, todo_id)

def delete(db: DBConnect, todo_id: int) -> bool:
    return data.delete(db, todo_id)