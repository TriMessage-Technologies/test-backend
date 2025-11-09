from fastapi import APIRouter, Form
from fastapi.responses import JSONResponse,Response
from schemas.schemas import User
router  = APIRouter()
fake_db = []
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