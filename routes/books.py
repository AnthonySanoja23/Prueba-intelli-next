import xlsxwriter
import io
import datetime

from fastapi import APIRouter
from config.db import conn
from models.books import books
from schemas.books import Book
from typing import List
from starlette.status import HTTP_204_NO_CONTENT
from sqlalchemy import func, select
from auth.auth_bearer import JWTBearer
from auth.auth_handler import signJWT
from fastapi import FastAPI, Body, Depends
from fastapi.responses import StreamingResponse
from fastapi.responses import Response

book = APIRouter()

def check_name_book(data:Book):
    book = conn.execute(books.select().where(books.c.title == data.title)).first()
    
    if book :
        return True
    else :
        return False



@book.get(
    "/books",
    tags=["books"],
    response_model=List[Book],
    description="Get a list of all Book",
    response_description='xlsx',
    dependencies=[Depends(JWTBearer())]
)
def get_books():
    booksdb = conn.execute(books.select()).fetchall()
    
    output = io.BytesIO()
    workbook = xlsxwriter.Workbook(output)
    worksheet = workbook.add_worksheet()

    rows = 1
    is_created = False
    
    for idx, book in enumerate(booksdb):
        dict_book = dict(book)
        dict_book["publication_date"]=dict_book["publication_date"].strftime('%m/%d/%Y')
        
        if is_created:
            columns=0
            for key, value in dict_book.items():
                worksheet.write(rows, columns,value)
                columns+=1
        else:
            columns = 0
            for key, value in dict_book.items(): 
                worksheet.write(0, columns,key)
                worksheet.write(rows, columns,value)
                columns+=1
                is_created = True
        rows+=1
    
    
    workbook.close()
    output.seek(0)
    
    headers = {
        'Content-Disposition': 'attachment; filename="books.xlsx"'
    }
    return StreamingResponse(output, headers=headers)




@book.post("/create-book/", 
           tags=["books"], 
           description="Create a new book",
           dependencies=[Depends(JWTBearer())]
)
def create_book(book: Book=Body(...)):
    
    if not check_name_book(book):
        new_book = {
            "id_book":book.id_book,
            "title": book.title, 
            "publication_date": book.publication_date,
        }
        result = conn.execute(books.insert().values(new_book))
        return conn.execute(books.select().where(books.c.id_book == result.lastrowid)).first()
    return {
        "error":"Book Exist!"
    }


@book.put(
    "/update-books/{id}", 
    tags=["books"], 
    response_model=Book, 
    description="Update a Book by Id",
    dependencies=[Depends(JWTBearer())]
)
def update_book(book: Book, id: int):
    conn.execute(
        books.update()
        .values(
            title=book.title,  
            publication_date=book.publication_date,
        )
        .where(books.c.id_book == id)
    )
    return conn.execute(books.select().where(books.c.id_book == id)).first()


@book.delete(
    "/delete-book/{id}",
    tags=["books"], 
    status_code=HTTP_204_NO_CONTENT,
    dependencies=[Depends(JWTBearer())]
)
def delete_book(id: int):
    conn.execute(books.delete().where(books.c.id_book == id))
    return Response(status_code=HTTP_204_NO_CONTENT)