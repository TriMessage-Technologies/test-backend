from pydantic import BaseModel


class User(BaseModel):
    username: str
    password: str
    email: str

class CreateRoomRequest(BaseModel):
    room_name: str
    password: str = None  # опциональный пароль
    max_users: int = 2

