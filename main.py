import os
import psycopg2
from fastapi import FastAPI

app = FastAPI()

@app.on_event("startup")
def init_db():
    db_url = os.environ.get("DATABASE_URL")
    if not db_url:
        print("DATABASE_URL نینە!")
        return
    
    try:
        conn = psycopg2.connect(db_url)
        cur = conn.cursor()
        cur.execute("CREATE TABLE IF NOT EXISTS users (username TEXT PRIMARY KEY, password TEXT)")
        conn.commit()
        cur.close()
        conn.close()
        print("داتابەیس ب سەرکەفتنێ هاتە گرێدان!")
    except Exception as e:
        print(f"کێشە د گرێدانێ دا: {e}")