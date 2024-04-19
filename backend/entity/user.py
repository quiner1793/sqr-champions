from pydantic import BaseModel
from typing import Optional


class User(BaseModel):
    id: Optional[int] = None
    username: str
    password: Optional[str] = None
    email: Optional[str] = None
