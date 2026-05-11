from fastapi import FastAPI, Depends, HTTPException, status, Query

app = FastAPI()

def verify_access(token: str = Query(...)):
    if token != "library-access":
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail="접근 권한이 없습니다.")
    return token

def get_db_session():
    db_data = {
        "1": "FastAPI 기초",
        "2": "Python 심화",
        "3": "의존성 주입 마스터"
    }
    return db_data

def search_filter(q: str = Query(None)):
    return q

def check_librarian_role(role: str = Query(None)):
    if role != "librarian":
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,detail="사서 권한이 필요합니다.")
    return role

@app.get("/books", dependencies=[Depends(verify_access)])
async def read_books(
        db=Depends(get_db_session),
        q=Depends(search_filter)
):
    if q:
        filtered_result = {k: v for k, v in db.items() if q in v}
        return {"result": filtered_result}

    return {"result": db}

@app.get("/book/{book_id}", dependencies=[Depends(verify_access)])
async def read_book_detail(
        book_id: str,
        db=Depends(get_db_session)
):
    book_title = db.get(book_id)

    if not book_title:
        raise HTTPException(status_code=404, detail="도서를 찾을 수 없습니다.")

    return {"id": book_id, "title": book_title}

@app.post("/books", dependencies=[Depends(verify_access), Depends(check_librarian_role)])
async def create_book():
    return {"message": "도서가 성공적으로 등록되었습니다."}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)