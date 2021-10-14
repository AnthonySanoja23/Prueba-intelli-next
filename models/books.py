import datetime
from sqlalchemy import Table,Column,ForeignKey
from sqlalchemy.sql.sqltypes import Integer,String,Date
from config.db import meta,engine
from config.db import conn
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship



books = Table("books",meta,
    Column("id_book",Integer,primary_key=True),
    Column("title",String(255)),
    Column("publication_date",Date()),     
)


meta.create_all(engine)
