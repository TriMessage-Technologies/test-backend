from fastapi import APIRouter, Form,WebSocket,WebSocketDisconnect
from fastapi.responses import Response
from fastapi.exceptions import HTTPException
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__)))
from schemas.schemas import User
from core.core import *
import json

class ConnectionManager:
    def __init__(self):
        # {room_id: [WebSocket1, WebSocket2, ...]}
        self.active_connections = {}
    
    async def connect(self, websocket: WebSocket, room_id: str):
        await websocket.accept()
        
        if room_id not in self.active_connections:
            self.active_connections[room_id] = []
        
        self.active_connections[room_id].append(websocket)
        print(f"Пользователь подключился к комнате {room_id}")
    
    def disconnect(self, websocket: WebSocket, room_id: str):
        if room_id in self.active_connections:
            self.active_connections[room_id].remove(websocket)
            
            # Если комната пуста — удаляем её
            if len(self.active_connections[room_id]) == 0:
                del self.active_connections[room_id]
        
        print(f"Пользователь отключился от комнаты {room_id}")
    
    async def send_personal_message(self, message: str, websocket: WebSocket):
        await websocket.send_text(message)
    
    async def broadcast_to_room(self, message: str, room_id: str, sender_ws: WebSocket = None):
        """Отправить сообщение всем в комнате, кроме отправителя"""
        if room_id in self.active_connections:
            dead_connections = []
            
            for connection in self.active_connections[room_id]:
                try:
                    if connection != sender_ws:
                        await connection.send_text(message)
                except:
                    dead_connections.append(connection)
            
            # Удаляем отключённые соединения
            for connection in dead_connections:
                self.disconnect(connection, room_id)
    
    async def broadcast_to_all_in_room(self, message: str, room_id: str):
        """Отправить сообщение всем в комнате, включая отправителя"""
        if room_id in self.active_connections:
            dead_connections = []
            
            for connection in self.active_connections[room_id]:
                try:
                    await connection.send_text(message)
                except:
                    dead_connections.append(connection)
            
            for connection in dead_connections:
                self.disconnect(connection, room_id)
    
    def get_room_users_count(self, room_id: str) -> int:
        """Количество пользователей в комнате"""
        if room_id in self.active_connections:
            return len(self.active_connections[room_id])
        return 0

manager = ConnectionManager()

router = APIRouter()
@router.post('/auth/register')
async def register(
        username: str = Form(...),
        email: str = Form(...),
        password: str = Form(...)
):
    user = User(username=username,email=email,password=password)
    try:
        add_user(user)
        return {"result":'success'}
    except:
        raise HTTPException(status_code=400,detail='something went wrong')
@router.post('/auth/login')
async def authorize(username:str = Form(),password:str = Form()):
    try:
        user = get_user(username=username,password=password)
    except:
        raise HTTPException(status_code=400,detail='something went wrong')
    if not user:
            raise HTTPException(status_code=404,detail='user not found')
    return {"result":'success'}
