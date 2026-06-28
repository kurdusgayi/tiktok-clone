from fastapi import FastAPI, Request, Form
from fastapi.templating import Jinja2Templates
from fastapi.responses import RedirectResponse

app = FastAPI()
templates = Jinja2Templates(directory="templates")

# ل ڤێرێ ئه‌م دێ لیسته‌کا داتایان هه‌بیت (بۆ ده‌ستپێکێ)
users = {}

@app.get("/signup")
def signup_page(request: Request):
    return templates.TemplateResponse("signup.html", {"request": request})

@app.post("/signup")
def register(username: str = Form(...), password: str = Form(...)):
    users[username] = password
    return RedirectResponse(url="/", status_code=303)