from fastapi import FastAPI
from routes.users import user
from routes.books import book
from routes.comments import comment
from routes.players import player



app = FastAPI()
app.include_router(user)
app.include_router(book)
app.include_router(comment)
app.include_router(player)






