from typing import Optional
from pydantic import BaseModel
from datetime import date


class User(BaseModel):
    id_user: Optional[str]
    username: str
    password: str
    first_name: str
    last_name: str


class UserLoginSchema(BaseModel):
    username: str 
    password: str 

    class Config:
        schema_extra = {
            "example": {
                "username": "username",
                "password": "password"
            }
        }        


