from fastapi import FastAPI, Request, WebSocket, WebSocketDisconnect
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from typing import Dict

app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")


class ConnectionManager:
    def __init__(self):
        self.active_connections: Dict[str, WebSocket] = {}

    async def connect(self, websocket: WebSocket, username: str):
        await websocket.accept()
        self.active_connections[username] = websocket

    def disconnect(self, username: str):
        del self.active_connections[username]

    async def broadcast(self, message: str, sender: str):
        for user, connection in self.active_connections.items():
            await connection.send_text(f"[{sender}] {message}")


# 귀멸의 칼날
@app.get("/", response_class=HTMLResponse)
async def root(request: Request):
    return templates.TemplateResponse("demon_slayer/sample.html", {"request": request})


@app.get("/quiz", response_class=HTMLResponse)
async def career(request: Request):
    return templates.TemplateResponse("demon_slayer/quiz.html", {"request": request})


@app.post("/quiz_result", response_class=HTMLResponse)
async def quiz_result(request: Request):
    form_data = await request.form()
    answer = ["해의 호흡", "카이가쿠", "토키토 무이치로", "카이가쿠", "연어", "코테츠", "무한열차", "오니기리"]
    score = 0
    for i in range(8):
        if answer[i] == form_data.get(f"question{i + 1}"):
            score += 1
    return templates.TemplateResponse("demon_slayer/quiz_result.html",
                                      {"request": request, "score": score, "category": get_score_category(score)})


@app.get("/archive", response_class=HTMLResponse)
async def character_archive(request: Request):
    return templates.TemplateResponse("demon_slayer/archive.html", {"request": request})


# 채팅방
@app.get("/chatroom", response_class=HTMLResponse)
async def chatroom(request: Request):
    return templates.TemplateResponse("demon_slayer/chat.html", {"request": request})


manager = ConnectionManager()


@app.websocket("/ws/{username}")
async def websocket_endpoint(websocket: WebSocket, username: str):
    await manager.connect(websocket, username)
    await manager.broadcast(f"{username}가 채팅방에 참여했습니다.", "* ")
    try:
        while True:
            data = await websocket.receive_text()
            await manager.broadcast(data, username)
    except WebSocketDisconnect:
        manager.disconnect(username)
        await manager.broadcast(f"{username}가 채팅방을 떠났습니다.", "* ")


@app.get("/participants")
async def show_participants():
    return list(manager.active_connections.keys())


# 커리어팀
@app.get("/career", response_class=HTMLResponse)
async def career(request: Request):
    return templates.TemplateResponse("career.html", {"request": request})


# TB프로젝트
@app.get("/adot/fashion/mycloset", response_class=HTMLResponse)
async def my_closet(request: Request):
    return templates.TemplateResponse("adot/mycloset.html", {"request": request})


@app.get("/adot/fashion/add_items", response_class=HTMLResponse)
async def add_items(request: Request):
    return templates.TemplateResponse("adot/add_items.html", {"request": request})


@app.get("/adot/fashion/save_completed", response_class=HTMLResponse)
async def save_completed(request: Request):
    return templates.TemplateResponse("adot/save_result.html", {"request": request})


@app.get("/adot/fashion/14230294", response_class=HTMLResponse)
async def item_detail(request: Request):
    return templates.TemplateResponse("adot/item_detail.html", {"request": request})


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
