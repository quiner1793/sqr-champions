import sqlite3
from datetime import timedelta

from fastapi import APIRouter, status, HTTPException
from starlette.requests import Request
from backend.entity import requests
from backend.entity.responses import StandardResponse
from backend.entity.token import Token
from backend.gateway.user_gw import UserGw
from fastapi.security import OAuth2PasswordRequestForm
from fastapi import Depends
from fastapi_another_jwt_auth import AuthJWT
from backend.config import config
import validators
import logging

router = APIRouter()



@router.post("/token", response_model=Token, include_in_schema=True)
async def login(
        request: Request,
        form: OAuth2PasswordRequestForm = Depends(),
        authorize: AuthJWT = Depends(),
):
    userGw = UserGw(request.app.state.db)
    try:
        user = await userGw.get_user(form)
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid username or password",
        )

    access_token = authorize.create_access_token(
        subject=user.username,
        expires_time=timedelta(minutes=config.auth_token_expire).seconds,
    )
    refresh_token = authorize.create_refresh_token(
        subject=user.username,
        expires_time=timedelta(
            minutes=config.auth_refresh_token_expire).seconds
    )

    return Token(access_token=access_token, refresh_token=refresh_token)


@router.post("/register", summary="Register", response_model=StandardResponse)
async def register(
        body: requests.RegisterRequest,
        request: Request,
) -> StandardResponse:
    if not validators.email(body.email):
        return StandardResponse(success=False, error="Invalid email")

    userGw = UserGw(request.app.state.db)

    try:
        await userGw.add_user(body)
    except sqlite3.Error as err:
        if err.sqlite_errorcode == sqlite3.SQLITE_CONSTRAINT_UNIQUE:
            field = str(err).replace("UNIQUE constraint failed: Users.", "")
            msg = f"Person with such {field} is already registered"
            return StandardResponse(success=False, error=msg)
        else:
            logging.error(f"error in register user: {err}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )

    return StandardResponse(success=True, error="")
