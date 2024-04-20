import os


class Config:
    server_host = os.getenv("SERVER_HOST")
    server_port = int(os.getenv("SERVER_PORT"))


config = Config()
