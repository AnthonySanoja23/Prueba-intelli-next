from sqlalchemy import create_engine, MetaData
from decouple import config


user_name = config("user_name")
password = config("MYSQL_ROOT_PASSWORD")
host = "db"
database_name = config("MYSQL_DATABASE")
attempts = 0

DATABASE = f"mysql+pymysql://{user_name}:{password}@{host}/{database_name}"

engine = create_engine(
    DATABASE,
    encoding="utf-8",
    echo=True,
    pool_pre_ping=True
)


meta = MetaData()
conn = engine.connect()

