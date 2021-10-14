from typing import Optional
from pydantic import BaseModel
from datetime import date

class Comment(BaseModel):
    id_comment: Optional[str]
    id_books: str
    text:str
    created_date:date
    id_users:str
    