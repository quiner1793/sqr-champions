from fastapi import FastAPI
from backend.config import Config
import sqlite3
from backend.gateway.db_gw import DatabaseGw


def add_source_events(app: FastAPI, config: Config) -> None:
    @app.on_event("startup")
    async def sql_lite_startup() -> None:
        connection = sqlite3.connect(config.db_name)
        db = DatabaseGw(connection)
        await db.create_tables()
        app.state.db = connection

    @app.on_event("shutdown")
    async def sql_lite_shutdown() -> None:
        app.state.db.close()
