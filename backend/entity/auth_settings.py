from pydantic import BaseModel


class AuthSettings(BaseModel):
    authjwt_secret_key: str
    authjwt_access_token_expires: int
    authjwt_refresh_token_expires: int
