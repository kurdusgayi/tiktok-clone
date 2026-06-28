import os
import psycopg2
from fastapi import FastAPI, Request, Form, Response, Cookie
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from fastapi.responses import RedirectResponse

app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

def get_db():
    return psycopg2.connect(os.environ.get("DATABASE_URL"))

@app.on_event("startup")
def startup():
    conn = get_db()
    cur = conn.cursor()
    # تێبله‌یا بکارئینه‌ران
    cur.execute('CREATE TABLE IF NOT EXISTS users (username TEXT PRIMARY KEY, password TEXT)')
    # تێبله‌یا Like و Comment
    cur.execute('CREATE TABLE IF NOT EXISTS interactions (id SERIAL PRIMARY KEY, username TEXT, type TEXT)')
    conn.commit()
    cur.close()
    conn.close()

@app.get("/")
def home(request: Request, username: str = Cookie(None)):
    return templates.TemplateResponse("index.html", {"request": request, "username": username})

@app.post("/signup")
def register(response: Response, username: str = Form(...), password: str = Form(...)):
    conn = get_db()
    cur = conn.cursor()
    cur.execute("INSERT INTO users (username, password) VALUES (%s, %s)", (username, password))
    conn.commit()
    response.set_cookie(key="username", value=username)
    return RedirectResponse(url="/", status_code=303)