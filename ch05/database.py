import sqlite3

def get_db():
    db = sqlite3.connect("store.db", check_same_thread=False)
    db.execute("CREATE TABLE IF NOT EXISTS snacks (id INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT, cost INTEGER, stock INTEGER)")
    try:
        yield db
    finally:
        db.close()