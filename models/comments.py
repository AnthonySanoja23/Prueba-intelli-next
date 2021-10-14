import datetime
from sqlalchemy import Table,Column,ForeignKey
from sqlalchemy.sql.sqltypes import Integer,String,Date
from config.db import meta,engine
from config.db import conn
from sqlalchemy.sql import func
from . import books,users


comments = Table("comment",meta,
    Column("id_comment",Integer,primary_key=True),
    Column("id_books",Integer,ForeignKey('books.id_book')),
    Column("text",String(255)),
    Column("created_date",Date()),
    Column("id_users",Integer,ForeignKey('users.id_user')),
    
)


meta.create_all(engine)