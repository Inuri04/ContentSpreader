from fastapi import FastAPI, UploadFile, File, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from .utils import process_video_file

app = FastAPI(title="KI-Content-Veredler")

templates = Jinja2Templates(directory="app/templates")
app.mount("/static", StaticFiles(directory="app/static"), name="static")


@app.get("/", response_class=HTMLResponse)
async def index(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


@app.post("/process", response_class=HTMLResponse)
async def process(request: Request, file: UploadFile = File(...)):
    contents = await file.read()
    result = process_video_file(contents)
    return templates.TemplateResponse("result.html", {"request": request, **result})

