import os
import psycopg2
import uvicorn
from fastapi import FastAPI, Request, Form, Response, Cookie
from fastapi.templating import Jinja2Templates
from fastapi.responses import RedirectResponse
from fastapi.staticfiles import StaticFiles

app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

# گرێدانا داتابه‌یسێ (Railway دێ ب خۆ DATABASE_URL دیار کەت)
def get_db_connection():
    return psycopg2.connect(os.environ.get("DATABASE_URL"))

# دروستکرنا تێبله‌یا بکارئینه‌ران
def init_db():
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute('''CREATE TABLE IF NOT EXISTS users 
                 (username TEXT PRIMARY KEY, password TEXT)''')
    conn.commit()
    cur.close()
    conn.close()

# ئه‌ڤێ ڤه‌که‌ ده‌مێ ته‌ یێ Database ل Railway گرێدای
# init_db() 

@app.get("/")
def read_root(request: Request, username: str = Cookie(None)):
    return templates.TemplateResponse(
        request=request, 
        name="index.html", 
        context={"username": username}
    )

@app.post("/signup")
def register(response: Response, username: str = Form(...), password: str = Form(...)):
    conn = get_db_connection()
    cur = conn.cursor()
    try:
        cur.execute("INSERT INTO users (username, password) VALUES (%s, %s)", (username, password))
        conn.commit()
        response.set_cookie(key="username", value=username)
    except Exception as e:
        print(f"Error: {e}")
    finally:
        cur.close()
        conn.close()
    return RedirectResponse(url="/", status_code=303)

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run("main:app", host="0.0.0.0", port=port)