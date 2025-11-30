from fastapi import APIRouter, Form
from fastapi.responses import JSONResponse,Response
from fastapi.exceptions import HTTPException
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__)))
from core.core import *
from schemas.schemas import User
router  = APIRouter()
fake_db = [] 
fake_servers = [{"123": "server1"}, {"1234": "server2"}, {"12345": "server3"}]

@router.post('/auth/register')
async def register(
    username: str = Form(...),
    email: str = Form(...),
    password: str = Form(...)
):
    
    # Регистрация пользователя
    user = User(username=username, password=password, email=email)
    await add_user(user=user)
    
    return Response(status_code=204)
@router.post('/auth/login')
async def authorize(username:str = Form(),password:str = Form()):
    try:
        b = get_user(username=username,password=password)
        if b:
            return Response(status_code=204)
        else:
            return HTTPException(status_code=401,detail='not authorized')
    except:
        raise HTTPException(status_code=400,detail='something went wrong')
router.get('/servers')
async def get_servs():
    return fake_servers

@router.get('/servers/{id}')
async def get_serv(id: str):
    for i in fake_servers:
        k = list(i.keys())[0]
        if k == id:
            val = i[k]
            return {"user_id": id, "user_server": val}   