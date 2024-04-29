import asyncio
import sqlite3
from unittest import IsolatedAsyncioTestCase

from backend.entity.user import User
from backend.gateway.db_gw import DatabaseGw
from backend.gateway.user_gw import UserGw


class TestUserGw(IsolatedAsyncioTestCase):
    def populate_user(
        self,
        limit: int,
        change_data: bool = True,
    ):
        for i in range(0, limit):
            self.db.cursor.execute(
                "INSERT INTO Users (username, password, email) "
                "VALUES (?, ?, ?)",
                (
                    self.user_data.username + (f"{i}" if change_data else ""),
                    self.user_data.password + (f"{i}" if change_data else ""),
                    self.user_data.email + (f"{i}" if change_data else ""),
                ),
            )

            self.db.con.commit()

    def await_func(self, func) -> None:
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(None)
        loop.run_until_complete(func)

    def setUp(self) -> None:
        self.connection = sqlite3.connect(":memory:")
        self.db = DatabaseGw(self.connection)
        # await self.db.create_tables()
        self.await_func(self.db.create_tables())
        self.user = UserGw(self.connection)
        self.user_data = User(
            username="qwerty", password="pass", email="a@mail.ru")

    def tearDown(self) -> None:
        del self.db
        del self.connection

    async def test_add_user(self):
        lastrowid = await self.user.add_user(self.user_data)
        self.db.cursor.execute(
            "SELECT * FROM Users WHERE id = ?", (str(lastrowid),))
        link_data = self.db.cursor.fetchone()
        assert (
            link_data[0] == lastrowid
            and link_data[1] == self.user_data.username
            and link_data[2] == self.user_data.password
            and link_data[3] == self.user_data.email
        )

    async def test_get_user_by_username(self):
        self.populate_user(3)
        result = await self.user.get_user_by_username("qwerty1")
        assert isinstance(result, User) and result.username == "qwerty1"

    async def test_get_user_by_not_existing_username(self):
        self.populate_user(3)
        result = await self.user.get_user_by_username("qwerty")
        assert result is None

    async def test_get_user(self):
        self.populate_user(3)
        result = await self.user.get_user(
            User(username="qwerty1", password="pass1"))
        assert (
            isinstance(result, User)
            and result.username == "qwerty1"
            and result.password == "pass1"
        )

    async def test_get_not_existing_user(self):
        self.populate_user(3)
        result = await self.user.get_user(
            User(username="qwerty", password="pass"))
        assert result is None

    async def test_get_username_by_id(self):
        self.populate_user(3)
        result = await self.user.get_username_by_id(2)
        assert result == "qwerty1"
