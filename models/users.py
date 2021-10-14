
from sqlalchemy import Table,Column
from sqlalchemy.sql.sqltypes import Integer,String,LargeBinary
from config.db import meta,engine
from config.db import conn


users = Table("users",meta,
    Column("id_user",Integer,primary_key=True),
    Column("username",String(255)),
    Column("password",LargeBinary(255)),
    Column("first_name",String(255)),
    Column("last_name",String(255)),             
)



meta.create_all(engine)





