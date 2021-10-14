from typing import Optional
from pydantic import BaseModel

class Player(BaseModel):
    id: Optional[str]
    name: str
    position: str
    nationality: str
    team: str