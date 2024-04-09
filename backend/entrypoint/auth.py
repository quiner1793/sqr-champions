import sqlite3

from fastapi import APIRouter, status, HTTPException
from starlette.requests import Request
from entity import auth_requests
from entity.auth_responses import AuthResponse

router = APIRouter()


@router.post("/login", summary="Login", response_model=AuthResponse)
async def login(
        body: auth_requests.LoginRequest,
        request: Request) -> AuthResponse:
    con = request.app.state.db
    cursor = con.cursor()
    try:
        cursor.execute('SELECT * FROM Users WHERE username = ? AND password = ?',
                       (body.username, body.password))
        user = cursor.fetchone()
        if user is None:
            return AuthResponse(success=False, error="No such user")
        return AuthResponse(success=True, error="")

    except sqlite3.Error:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
        )


@router.post("/register", summary="Register", response_model=AuthResponse)
async def register(
        body: auth_requests.RegisterRequest,
        request: Request,
) -> AuthResponse:
    con = request.app.state.db
    cursor = con.cursor()
    try:
        cursor.execute('INSERT INTO Users (username, password, email) '
                       'VALUES (?, ?, ?)',
                       (body.username, body.password, body.email))

        con.commit()

    except sqlite3.Error as err:
        if err.sqlite_errorcode == sqlite3.SQLITE_CONSTRAINT_UNIQUE:
            field = str(err).replace("UNIQUE constraint failed: Users.", "")
            msg = f"Person with such {field} is already registered"
            return AuthResponse(success=False, error=msg)
        else:
            raise HTTPException(
                status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            )

    return AuthResponse(success=True, error="")
