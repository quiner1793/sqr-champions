from datetime import timedelta

from backend.entity.user import User
from fastapi import Depends
from fastapi_another_jwt_auth import AuthJWT
from fastapi_another_jwt_auth.exceptions import AuthJWTException
from fastapi import HTTPException
from fastapi import status
from fastapi import APIRouter
from backend.entity.auth_settings import AuthSettings
from backend.config import config

from fastapi.security import OAuth2PasswordBearer

router = APIRouter()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/token")


@AuthJWT.load_config
def get_config():
    return AuthSettings(
        authjwt_secret_key=config.auth_secret_key,
        authjwt_access_token_expires=timedelta(
            minutes=config.auth_token_expire).seconds,
        authjwt_refresh_token_expires=timedelta(
            minutes=config.auth_refresh_token_expire).seconds,
    )


async def get_current_user(
        authorize: AuthJWT = Depends(),
        _: str = Depends(oauth2_scheme)
) -> User:
    try:
        username: str = authorize.get_jwt_subject()
    except AuthJWTException:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token"
        )

    return User(username=username)
