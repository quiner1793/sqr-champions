import os
from dotenv import load_dotenv


class Config:
    load_dotenv()
    server_host = os.getenv("SERVER_HOST")
    server_port = int(os.getenv("SERVER_PORT"))
    db_name = os.getenv("DB_NAME")
    auth_secret_key = os.getenv("AUTH_SECRET_KEY")
    auth_token_expire = int(os.getenv("AUTH_TOKEN_EXPIRE"))
    auth_refresh_token_expire = int(os.getenv("AUTH_REFRESH_TOKEN_EXPIRE"))


config = Config()
