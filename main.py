import os
import psycopg2
from fastapi import FastAPI, Request, Form, Response, Cookie
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from fastapi.responses import RedirectResponse

app = FastAPI()

# Mount static files and templates
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

# Function to connect to the database
def get_db_connection():
    #DATABASE_URL-ا تە دڤێت ل Variables یێن Railway بیت
    db_url = os.environ.get("DATABASE_URL")
    return psycopg2.connect(db_url)

@app.on_event("startup")
def init_db():
    try:
        conn = get_db_connection()
        cur = conn.cursor()
        # دروستکرنا تێبله‌یا بکارئینه‌ران ئه‌گه‌ر نه‌بیت
        cur.execute("CREATE TABLE IF NOT EXISTS users (username TEXT PRIMARY KEY, password TEXT)")
        conn.commit()
        cur.close()
        conn.close()
        print("Database initialized successfully!")
    except Exception as e:
        print(f"Error initializing database: {e}")

@app.get("/")
def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

# تو دشێی هه‌ر پشکێن دی ل ڤێرێ زێده‌ بکه‌ی