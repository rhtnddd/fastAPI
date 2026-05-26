# Step 7. 최종 실행 파일 (main.py)
# 모든 준비가 끝났습니다. 라우터와 템플릿을 연결하고 서버를 실행합니다!
# main.py
import uvicorn
from fastapi import FastAPI
from starlette.requests import Request
from starlette.templating import Jinja2Templates
# from contextlib import asynccontextmanager # DB 연결 라이프사이클 관리에서 더 이상 필요 없음

from web import todo
import service.todo as todo_service
# from data.todo import db # 전역 DB 객체는 더 이상 사용하지 않음
from data.todo import DBConnect  # index 함수에서 로컬 DBConnect 사용을 위해 임포트

# --- FastAPI 애플리케이션 라이프사이클 관리 ---
# DB 연결 관리가 각 요청마다 이루어지므로, 이 lifespan은 더 이상 필요 없음
# @asynccontextmanager
# async def lifespan(app: FastAPI):
#     print("🚀 FastAPI 애플리케이션 시작: DB 연결 초기화...")
#     yield
#     print("👋 FastAPI 애플리케이션 종료: DB 연결 해제...")
#     db.close()

# FastAPI 앱 인스턴스 생성, lifespan 제거
app = FastAPI()

# 웨이터(Router)를 식당(App)에 등록
app.include_router(todo.router)

# 화면 인테리어(Template) 폴더 지정
templates = Jinja2Templates(directory="templates/")


@app.get("/")
async def index(request: Request):
    # 루트 엔드포인트는 의존성 주입을 사용하지 않으므로, 로컬에서 DB 연결을 생성하고 관리합니다.
    db_local = DBConnect(check_same_thread=False)  # check_same_thread=False 설정
    try:
        todos = todo_service.find_all(db_local)  # 로컬 DB 연결 객체를 전달
    finally:
        db_local.close()  # 연결 닫기

    return templates.TemplateResponse(
        request=request,
        name="index.html",
        context={"todos": todos}
    )


if __name__ == "__main__":
    # 파이참 터미널에서 python main.py 로 실행하세요!
    print("🚀 FastAPI 서버를 시작합니다... (http://localhost:8000)")
    # reload=True를 사용하면 파일 변경 시 자동 재시작되는데,
    # 이때 DB 연결이 제대로 닫히지 않아 PermissionError가 발생할 수 있습니다.
    # 이제 DB 연결이 요청마다 관리되므로 이 문제가 완화됩니다.
    uvicorn.run("main:app", host='0.0.0.0', port=8000, reload=True)