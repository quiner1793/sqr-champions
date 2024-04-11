from fastapi import FastAPI
from backend.config import Config
import sqlite3


def add_source_events(app: FastAPI, config: Config) -> None:
    @app.on_event("startup")
    async def sql_lite_startup() -> None:
        connection = sqlite3.connect(config.db_name)
        await create_tables(connection)
        app.state.db = connection

    @app.on_event("shutdown")
    async def redis_shutdown() -> None:
        app.state.db.close()


async def create_tables(con: sqlite3.Connection) -> None:
    cursor = con.cursor()
    cursor.execute('''
                CREATE TABLE IF NOT EXISTS Users (
                id INTEGER PRIMARY KEY,
                username TEXT NOT NULL UNIQUE,
                password TEXT NOT NULL,
                email TEXT NOT NULL UNIQUE
                )
                ''')

    cursor.execute('''
                    CREATE TABLE IF NOT EXISTS Links (
                    id INTEGER PRIMARY KEY,
                    link TEXT NOT NULL UNIQUE,
                    title TEXT NOT NULL,
                    platform TEXT NOT NULL
                    )
                    ''')

    cursor.execute('''
                CREATE TABLE IF NOT EXISTS Feedback (
                id INTEGER PRIMARY KEY,
                user_id INTEGER NOT NULL,
                link_id INTEGER NOT NULL,
                comment TEXT NOT NULL,
                date TEXT NOT NULL,
                FOREIGN KEY(user_id) REFERENCES Users(id),
                FOREIGN KEY(link_id) REFERENCES Links(id)
                )
                ''')
    con.commit()
