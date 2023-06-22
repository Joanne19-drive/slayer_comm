from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles

app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")


@app.get("/", response_class=HTMLResponse)
async def root(request: Request):
    return templates.TemplateResponse("sample.html", {"request": request})


@app.get("/career", response_class=HTMLResponse)
async def career(request: Request):
    return templates.TemplateResponse("career.html", {"request": request})


@app.get("/quiz", response_class=HTMLResponse)
async def career(request: Request):
    return templates.TemplateResponse("quiz.html", {"request": request})


@app.post("/quiz_result", response_class=HTMLResponse)
async def quiz_result(request: Request):
    form_data = await request.form()
    answer = ["해의 호흡", "카이가쿠", "토키토 무이치로", "카이가쿠", "연어", "코테츠", "무한열차", "오니기리"]
    score = 0
    for i in range(8):
        if answer[i] == form_data.get(f"question{i + 1}"):
            score += 1
    return templates.TemplateResponse("quiz_result.html", {"request": request, "score": score, "category": get_score_category(score)})


def get_score_category(score):
    if score < 2:
        return "lowest"
    elif score < 4:
        return "low"
    elif score < 6:
        return "medium"
    elif score < 8:
        return "high"
    else:
        return "excellent"
