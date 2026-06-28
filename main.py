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

def get_db_connection():
    return psycopg2.connect(os.environ.get("DATABASE_URL"))

@app.on_event("startup")
def startup():
    conn = get_db_connection()
    cur = conn.cursor()
    # تێبله‌یا بکارئینه‌ران
    cur.execute('CREATE TABLE IF NOT EXISTS users (username TEXT PRIMARY KEY, password TEXT)')
    # تێبله‌یا Like و Comment
    cur.execute('CREATE TABLE IF NOT EXISTS interactions (id SERIAL PRIMARY KEY, username TEXT, type TEXT)')
    conn.commit()
    cur.close()
    conn.close()

@app.get("/")
def read_root(request: Request, username: str = Cookie(None)):
    return templates.TemplateResponse("index.html", {"request": request, "username": username})

@app.post("/signup")
def register(response: Response, username: str = Form(...), password: str = Form(...)):
    try:
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute("INSERT INTO users (username, password) VALUES (%s, %s)", (username, password))
        conn.commit()
        response.set_cookie(key="username", value=username)
    except:
        pass # ئه‌گه‌ر ناڤێ بکارئینه‌ری یێ هه‌ی
    return RedirectResponse(url="/", status_code=303)

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=int(os.environ.get("PORT", 8000)))