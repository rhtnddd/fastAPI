from fastapi import FastAPI, Depends
from fastapi.responses import RedirectResponse, HTMLResponse
from pydantic import BaseModel, Field
from typing import List
import sqlite3
from database import get_db

app = FastAPI()


class SnackCreate(BaseModel):
    name: str = Field(..., min_length=2)
    cost: int = Field(..., gt=0)
    stock: int = Field(..., gt=0)


class SnackResponse(BaseModel):
    name: str
    selling_price: int


@app.post("/snacks")
def create_snack(snack: SnackCreate, db: sqlite3.Connection = Depends(get_db)):
    cursor = db.cursor()
    cursor.execute(
        "INSERT INTO snacks (name, cost, stock) VALUES (?, ?, ?)",
        (snack.name, snack.cost, snack.stock)
    )
    db.commit()
    return RedirectResponse(url="/snacks/html", status_code=302)


@app.get("/snacks", response_model=List[SnackResponse])
def list_snacks_json(db: sqlite3.Connection = Depends(get_db)):
    cursor = db.cursor()
    cursor.execute("SELECT name, cost FROM snacks")
    rows = cursor.fetchall()
    return [{"name": row[0], "selling_price": row[1] + 500} for row in rows]


@app.get("/snacks/html", response_class=HTMLResponse)
def list_snacks_html(db: sqlite3.Connection = Depends(get_db)):
    cursor = db.cursor()
    cursor.execute("SELECT name, cost FROM snacks")
    rows = cursor.fetchall()

    table_rows = ""
    for row in rows:
        name = row[0]
        selling_price = row[1] + 500
        table_rows += f"<tr><td>{name}</td><td>{selling_price}원</td></tr>"

    html_content = f"""
    <html>
        <body>
            <h2>학급 매점 간식 목록</h2>
            <table border='1'>
                <thead>
                    <tr><th>이름</th><th>판매가</th></tr>
                </thead>
                <tbody>
                    {table_rows}
                </tbody>
            </table>
        </body>
    </html>
    """
    return HTMLResponse(content=html_content)