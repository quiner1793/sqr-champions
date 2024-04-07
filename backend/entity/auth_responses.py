from pydantic import BaseModel


class AuthResponse(BaseModel):
    success: bool
    error: str
