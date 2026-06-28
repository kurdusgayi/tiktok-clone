import os
import sqlite3
import uvicorn
from fastapi import FastAPI, Request, Form, Response, Cookie
from fastapi.templating import Jinja2Templates
from fastapi.responses import RedirectResponse
from fastapi.staticfiles import StaticFiles

app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

# دروستکرنا Databaseـێ
def init_db():
    conn = sqlite3.connect('users.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS users (username TEXT PRIMARY KEY, password TEXT)''')
    conn.commit()
    conn.close()

init_db()

@app.get("/")
def read_root(request: Request, username: str = Cookie(None)):
    return templates.TemplateResponse(
        request=request, 
        name="index.html", 
        context={"username": username}
    )

@app.get("/signup")
def signup_page(request: Request):
    return templates.TemplateResponse(request=request, name="signup.html")

@app.post("/signup")
def register(response: Response, username: str = Form(...), password: str = Form(...)):
    conn = sqlite3.connect('users.db')
    c = conn.cursor()
    try:
        c.execute("INSERT INTO users VALUES (?, ?)", (username, password))
        conn.commit()
        # پاشی تومارکرنێ، خودکار Login بکه‌
        response.set_cookie(key="username", value=username)
        return RedirectResponse(url="/", status_code=303)
    except sqlite3.IntegrityError:
        return "ئه‌ڤ ناڤه‌ یێ هه‌ی!"
    finally:
        conn.close()

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run("main:app", host="0.0.0.0", port=port)