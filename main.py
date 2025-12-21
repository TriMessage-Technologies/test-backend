from fastapi import FastAPI, Form, Depends, HTTPException
from fastapi.responses import FileResponse
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from typing import Optional
import uuid
import os

app = FastAPI(title="Chat Rooms", version="1.0")
app.mount("/static", StaticFiles(directory="frontend"), name="static")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

users_db = []
rooms_db = []


# Главная страница
@app.get("/")
async def serve_index():
    return FileResponse("frontend/index.html")


@app.post("/api/register")
async def register(
        username: str = Form(...),
        email: str = Form(...),
        password: str = Form(...)
):
    for user in users_db:
        if user["username"] == username:
            raise HTTPException(status_code=400, detail="Имя пользователя уже существует")

    new_user = {
        "id": str(uuid.uuid4()),
        "username": username,
        "email": email,
        "password": password
    }
    users_db.append(new_user)

    return {
        "success": True,
        "message": "Регистрация успешна",
        "user": {"username": username, "email": email}
    }


@app.post("/api/login")
async def login(
        username: str = Form(...),
        password: str = Form(...)
):
    for user in users_db:
        if user["username"] == username and user["password"] == password:
            return {
                "success": True,
                "message": "Авторизация успешна",
                "user": {"username": username, "email": user["email"]}
            }

    raise HTTPException(status_code=401, detail="Неверное имя пользователя или пароль")


@app.get("/api/rooms")
async def get_rooms():
    return rooms_db


@app.post("/api/rooms/create")
async def create_room(
        room_name: str = Form(...),
        password: Optional[str] = Form(None),
        max_users: int = Form(2)
):
    room_id = str(uuid.uuid4())[:8]
    new_room = {
        "id": room_id,
        "name": room_name,
        "creator": "anonymous",
        "has_password": password is not None and password != "",
        "password": password if password else None,
        "max_users": max_users,
        "current_users": 0,
        "users": []
    }
    rooms_db.append(new_room)

    return {
        "success": True,
        "room": new_room,
        "message": "Комната создана успешно"
    }


@app.post("/api/rooms/{room_id}/join")
async def join_room(
        room_id: str,
        password: Optional[str] = Form(None),
        username: str = Form(...)
):
    for room in rooms_db:
        if room["id"] == room_id:
            if room["has_password"]:
                if password is None or password != room.get("password", ""):
                    raise HTTPException(status_code=403, detail="Неверный пароль")

            if room["current_users"] >= room["max_users"]:
                raise HTTPException(status_code=400, detail="Комната заполнена")

            if username in room["users"]:
                raise HTTPException(status_code=400, detail="Вы уже в этой комнате")

            room["users"].append(username)
            room["current_users"] += 1

            return {
                "success": True,
                "room": room,
                "message": f"Вы присоединились к комнате '{room['name']}'"
            }

    raise HTTPException(status_code=404, detail="Комната не найдена")


@app.get("/api/debug/users")
async def debug_users():
    return {"count": len(users_db), "users": users_db}


@app.get("/api/debug/rooms")
async def debug_rooms():
    return {"count": len(rooms_db), "rooms": rooms_db}


if __name__ == "__main__":
    import uvicorn

    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=False)
