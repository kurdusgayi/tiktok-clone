import os
import uvicorn
from fastapi import FastAPI, Request, Form
from fastapi.templating import Jinja2Templates
from fastapi.responses import RedirectResponse
from fastapi.staticfiles import StaticFiles

app = FastAPI()

# ئه‌ڤه‌ بۆ ناسینا فایلێن ستاتیک و تێمپلێتان
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

users = {}

@app.get("/")
def read_root(request: Request):
    return templates.TemplateResponse(
        request=request, 
        name="index.html"
    )

@app.get("/signup")
def signup_page(request: Request):
    return templates.TemplateResponse(
        request=request, 
        name="signup.html"
    )

@app.post("/signup")
def register(username: str = Form(...), password: str = Form(...)):
    users[username] = password
    return RedirectResponse(url="/", status_code=303)

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run("main:app", host="0.0.0.0", port=port)