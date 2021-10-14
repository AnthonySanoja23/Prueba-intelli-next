import xlsxwriter
import io
import datetime

from fastapi import APIRouter
from config.db import conn
from models.comments import comments
from schemas.comments import Comment
from typing import List
from starlette.status import HTTP_204_NO_CONTENT
from sqlalchemy import func, select
from auth.auth_bearer import JWTBearer
from auth.auth_handler import signJWT
from fastapi import FastAPI, Body, Depends
from fastapi.responses import StreamingResponse,Response



comment = APIRouter()



@comment.get(
    "/comments",
    tags=["comments"],
    response_model=List[Comment],
    description="Get a list of all Comment",
    dependencies=[Depends(JWTBearer())]
)
def get_comments():
    commentsdb = conn.execute(comments.select()).fetchall()
    output = io.BytesIO()
    workbook = xlsxwriter.Workbook(output)
    worksheet = workbook.add_worksheet()

    rows = 1
    is_created = False
    
    for idx, comment in enumerate(commentsdb):
        dict_comment = dict(comment)
        dict_comment["created_date"]=dict_comment["created_date"].strftime('%m/%d/%Y')
        
        if is_created:
            columns=0
            for key, value in dict_comment.items():
                worksheet.write(rows, columns,value)
                columns+=1
        else:
            columns = 0
            for key, value in dict_comment.items(): 
                worksheet.write(0, columns,key)
                worksheet.write(rows, columns,value)
                columns+=1
                is_created = True
        rows+=1
    
    
    workbook.close()
    output.seek(0)
    
    headers = {
        'Content-Disposition': 'attachment; filename="comment.xlsx"'
    }
    return StreamingResponse(output, headers=headers)




@comment.post(
    "/create-comment/", 
    tags=["comments"], 
    response_model=Comment, 
    description="Create a new Comment",
    dependencies=[Depends(JWTBearer())]
)
def create_comment(comment: Comment):
    new_comment = {
        "id_comment":comment.id_comment,
        "id_books":comment.id_books,
        "text":comment.text,
        "created_date":comment.created_date,
        "id_users":comment.id_users
    }
    result = conn.execute(comments.insert().values(new_comment))
    return conn.execute(comments.select().where(comments.c.id_comment == result.lastrowid)).first()


@comment.put(
    "/update-comments/{id}", 
    tags=["comments"], 
    response_model=Comment, 
    description="Update a Comment by Id",
    dependencies=[Depends(JWTBearer())]
)
def update_comment(comment: Comment, id: int):
    conn.execute(
        comments.update()
        .values(
            id_books=comment.id_books,
            text=comment.text, 
            created_date=comment.created_date,
            id_users=comment.id_users
        )
        .where(comments.c.id_comment == id)
    )
    return conn.execute(comments.select().where(comments.c.id_comment == id)).first()


@comment.delete(
    "/delete-comment/{id}", 
    tags=["comments"], 
    status_code=HTTP_204_NO_CONTENT,
    dependencies=[Depends(JWTBearer())]
)
def delete_comment(id: int):
    conn.execute(comments.delete().where(comments.c.id_comment == id))
    return Response(status_code=HTTP_204_NO_CONTENT)