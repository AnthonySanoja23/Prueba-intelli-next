from typing import Optional
from pydantic import BaseModel
from datetime import date

class Book(BaseModel):
    id_book: Optional[str]
    title: str
    publication_date: date