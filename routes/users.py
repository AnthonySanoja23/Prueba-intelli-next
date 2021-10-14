import bcrypt
import xlsxwriter
import io

from sqlalchemy.sql.elements import Null
from sqlalchemy.sql.expression import false
from fastapi import APIRouter
from config.db import conn
from models.users import users
from schemas.users import User,UserLoginSchema
from typing import List
from starlette.status import HTTP_204_NO_CONTENT
from sqlalchemy import func, select
from auth.auth_bearer import JWTBearer
from auth.auth_handler import signJWT
from fastapi import FastAPI, Body, Depends
from fastapi.responses import StreamingResponse,Response



user = APIRouter()

def check_username(data: UserLoginSchema):
    user = conn.execute(users.select().where(users.c.username == data.username)).first()
    
    if user :
        return True
    else :
        return False    


def check_user(data: UserLoginSchema):
    user = conn.execute(users.select().where(users.c.username == data.username)).first()

    if user :
        return bcrypt.checkpw(data.password.encode(), user.password)
    else :
        return False

    
@user.get(
    "/users",
    tags=["users"],
    response_model=List[User],
    description="Get a list of all users",
    response_description='xlsx',
    dependencies=[Depends(JWTBearer())]
)
def get_users():
    userdb = conn.execute(users.select()).fetchall()
    
    output = io.BytesIO()
    workbook = xlsxwriter.Workbook(output)
    worksheet = workbook.add_worksheet()

    rows = 1
    is_created = False
    
    for idx, user in enumerate(userdb):
        dict_user = dict(user)
        dict_user["password"] = dict_user["password"].decode(encoding='UTF-8')
        
        if is_created:
            columns=0
            for key, value in dict_user.items():
                worksheet.write(rows, columns,value)
                columns+=1
        else:
            columns = 0
            for key, value in dict_user.items(): 
                worksheet.write(0, columns,key)
                worksheet.write(rows, columns,value)
                columns+=1
                is_created = True
        rows+=1
    
    
    workbook.close()
    output.seek(0)
    
    headers = {
        'Content-Disposition': 'attachment; filename="users.xlsx"'
    }
    return StreamingResponse(output, headers=headers)


@user.post("/create_user/", 
           tags=["users"],
           description="Create a new user",
           
)
def create_user(user: User=Body(...)):
    
    if not check_username(user):
        new_user = {
            "id_user":user.id_user,
            "username": user.username, 
            "first_name": user.first_name,
            "last_name": user.last_name
        }
        
        pass_byte = user.password.encode()
        sal = bcrypt.gensalt()
        pass_hasheada = bcrypt.hashpw(pass_byte,sal)
        new_user["password"] = pass_hasheada
    
        result = conn.execute(users.insert().values(new_user))
        return signJWT(user.username)
    
    return {
        "error":"Username Exist!"
    }

@user.post("/user/login", tags=["users"])
async def user_login(user: UserLoginSchema = Body(...)):
    if check_user(user):
        return signJWT(user.username)
    return {
        "error": "Wrong login details!"
    }


@user.put(
    "/update_users/{id}",
    tags=["users"], 
    response_model=User, 
    description="Update a User by Id",
    dependencies=[Depends(JWTBearer())]
)
def update_user(user: User, id: int):
    
    pass_byte = user.password.encode()
    sal = bcrypt.gensalt()
    pass_hasheada = bcrypt.hashpw(pass_byte,sal)
    user.password = pass_hasheada
    
    conn.execute(
        users.update()
        .values(
            username=user.username,  
            password=user.password,
            first_name=user.first_name,
            last_name=user.last_name,
        )
        .where(users.c.id_user == id)
    )
    return conn.execute(users.select().where(users.c.id_user == id)).first()


@user.delete(
    "/delete_users/{id}", 
    tags=["users"], 
    status_code=HTTP_204_NO_CONTENT,
    dependencies=[Depends(JWTBearer())]
)

def delete_user(id: int):
    conn.execute(users.delete().where(users.c.id_user == id))
    return Response(status_code=HTTP_204_NO_CONTENT)




       


        

    