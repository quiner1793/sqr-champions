import os
from dotenv import load_dotenv


class Config:
    load_dotenv()
    server_host = os.getenv("SERVER_HOST")
    server_port = int(os.getenv("SERVER_PORT"))
    db_name = os.getenv("DB_NAME")


config = Config()
