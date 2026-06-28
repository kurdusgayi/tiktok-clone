from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
import sqlite3

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# ڕێکا لاپه‌رێ سه‌ره‌کی
@app.get("/")
def read_root():
    return FileResponse("index.html")

# چێکرنا تابلۆیان ب شێوه‌یه‌کێ ڕێک
def init_db():
    conn = sqlite3.connect('tiktok.db')
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS videos 
                      (id INTEGER PRIMARY KEY, title TEXT, url TEXT, likes INTEGER DEFAULT 0)''')
    cursor.execute('''CREATE TABLE IF NOT EXISTS comments 
                      (id INTEGER PRIMARY KEY, video_id INTEGER, text TEXT)''')
    conn.commit()
    conn.close()

init_db()

@app.get("/get-videos")
def get_all_videos():
    conn = sqlite3.connect('tiktok.db')
    cursor = conn.cursor()
    cursor.execute("SELECT id, title, url, likes FROM videos")
    data = cursor.fetchall()
    conn.close()
    return {"videos": data}

@app.post("/like/{video_id}")
def like_video(video_id: int):
    conn = sqlite3.connect('tiktok.db')
    cursor = conn.cursor()
    cursor.execute("UPDATE videos SET likes = likes + 1 WHERE id = ?", (video_id,))
    conn.commit()
    conn.close()
    return {"status": "success"}

@app.post("/add-comment/{video_id}")
def add_comment(video_id: int, text: str):
    conn = sqlite3.connect('tiktok.db')
    cursor = conn.cursor()
    cursor.execute("INSERT INTO comments (video_id, text) VALUES (?, ?)", (video_id, text))
    conn.commit()
    conn.close()
    return {"status": "success"}