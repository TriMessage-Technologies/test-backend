from fastapi import APIRouter, Form
from fastapi.responses import JSONResponse,Response
from schemas.schemas import User
from fastapi.exceptions import HTTPException
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
    fake_db.append(user)
    print("Текущая база:", fake_db)
    
    return Response(status_code=204)
@router.get('/auth/login')
async def authorize(username:str = Form(),password:str = Form()):
    for user in fake_db:
        if user.username == username and user.password == password:
            return Response(status_code=204)
    return HTTPException(detail='Not authorized',status_code=401)
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