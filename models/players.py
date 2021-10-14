from sqlalchemy import Table,Column
from sqlalchemy.sql.sqltypes import Integer,String
from config.db import meta,engine
from config.db import conn


players = Table("players",meta,
    Column("id",Integer,primary_key=True),
    Column("name",String(255)),
    Column("position",String(255)),
    Column("nationality",String(255)),
    Column("team",String(255)),
    )



meta.create_all(engine)
