from fastapi import FastAPI, Request
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles

app = FastAPI()

# ڤێ په‌لدانکا templatesـێ بۆ HTML فایلان دیار دکه‌ت
templates = Jinja2Templates(directory="templates")

# ڤێ په‌لدانکا staticـێ بۆ CSS و وێنان دیار دکه‌ت
app.mount("/static", StaticFiles(directory="static"), name="static")

@app.get("/")
def read_root(request: Request):
    # دێ فایلا index.html نیشان ده‌ت
    return templates.TemplateResponse("index.html", {"request": request})