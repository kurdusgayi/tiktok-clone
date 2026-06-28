import os
import uvicorn
from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def read_root():
    return {"message": "Hello from TikTok Clone!"}

if __name__ == "__main__":
    # Railway دێ ب ڤێ رێزێ پۆرتی دابین کەت
    port = int(os.environ.get("PORT", 8080))
    uvicorn.run("main:app", host="0.0.0.0", port=port)