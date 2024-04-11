from pydantic import BaseModel
from typing import Optional


class Link(BaseModel):
    id: Optional[int] = None
    link: str
    title: str
    platform: str
