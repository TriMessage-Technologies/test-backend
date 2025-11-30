import asyncpg
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__)))
from schemas.schemas import User
async def add_user(user:User):
    conn = await asyncpg.connect(host='localhost',user='postgres',password='31591',database='fastapi_base')
    tr =  conn.transaction()
    try:
        await tr.start()
        await conn.execute('INSERT INTO \"Users\"(username,email,password) VALUES($1,$2,$3)',user.username,user.email,user.password)
        await tr.commit()
    except Exception as e:
        print(f'failed:{e}')
        await tr.rollback()
    await conn.close()
async def get_user(username:str,password:str):
    conn = await asyncpg.connect(host='localhost',user='postgres',password='31591',database='fastapi_base')
    tr =  conn.transaction()
    try:
        await tr.start()
        user  = await conn.fetchrow('SELECT username,password,email FROM \"Users\"  WHERE username = $1 and password = $2',username,password)
        await tr.commit()
    except Exception as e:
        print(f'failed:{e}')
        user = None
        await tr.rollback()
    await conn.close()
    if user:
        return tuple(user)