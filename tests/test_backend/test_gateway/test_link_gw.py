import asyncio
import sqlite3
from unittest import IsolatedAsyncioTestCase

from backend.entity.link import Link
from backend.gateway.db_gw import DatabaseGw
from backend.gateway.link_gw import LinkGw


class TestLinkGw(IsolatedAsyncioTestCase):
    def populate_link(
        self,
        limit: int,
        change_link_and_platform: bool = True,
        change_title: bool = True,
    ):
        for i in range(0, limit):
            self.db.cursor.execute(
                "INSERT INTO Links (link, title, platform) "
                "VALUES (?, ?, ?)",
                (
                    (
                        self.links[i]
                        if change_link_and_platform
                        else self.link_data.link
                    ),
                    self.link_data.title + (f"{i}" if change_title else ""),
                    (
                        self.platforms[i]
                        if change_link_and_platform
                        else self.link_data.platform
                    ),
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
        self.link = LinkGw(self.connection)
        self.links = [
            "https://stackoverflow.com/questions/23033939",
            "https://github.com/quiner1793/sqr-champions",
            "https://www.youtube.com/watch?v=tBTNMo77h2Q",
        ]
        self.platforms = ["stackoverflow", "github", "youtube"]
        self.link_data = Link(
            link=self.links[0],
            title="some video title",
            platform=self.platforms[0]
        )

    def tearDown(self) -> None:
        del self.db
        del self.connection

    async def test_add_link(self):
        lastrowid = await self.link.add_link(self.link_data)
        self.db.cursor.execute(
            "SELECT * FROM Links WHERE id = ?", (lastrowid,))
        link_data = self.db.cursor.fetchone()
        assert (
            link_data[0] == lastrowid
            and link_data[1] == self.link_data.link
            and link_data[2] == self.link_data.title
            and link_data[3] == self.link_data.platform
        )

    async def test_get_link_data_by_link(self):
        self.populate_link(1, change_title=False)
        result = await self.link.get_link_data_by_link(self.link_data.link)
        self.link_data.id = 1
        assert isinstance(result, Link) and result == self.link_data

    async def test_get_link_data_by_link_no_data(self):
        result = await self.link.get_link_data_by_link(self.link_data.link)
        assert result is None

    async def test_get_link_data_by_link_id(self):
        self.populate_link(3)
        result = await self.link.get_link_data_by_link_id(2)
        assert (
            isinstance(result, Link)
            and result.id == 2
            and result.link == self.links[1]
            and result.title == self.link_data.title + "1"
            and result.platform == self.platforms[1]
        )

    async def test_get_link_data_by_link_id_no_data(self):
        result = await self.link.get_link_data_by_link_id(1)
        assert result is None

    async def test_get_links_by_query_title(self):
        self.populate_link(3)
        result = await self.link.get_links_by_query("some video title")
        assert len(result) == 3

    async def test_get_links_by_query_platform(
        self,
    ):  # TODO check, sometimes not passed
        self.populate_link(3)
        result = await self.link.get_links_by_query("you")
        assert (
            len(result) == 1
            and isinstance(result[0], Link)
            and result[0].title == self.link_data.title + "2"
            and result[0].platform == self.platforms[2]
        )

    async def test_no_link_for_query(self):
        self.populate_link(2)
        result = await self.link.get_links_by_query("true")
        assert len(result) == 0

    async def test_get_latest(self):
        self.populate_link(3)
        result = await self.link.get_latest(2)
        assert (
            len(result) == 2
            and isinstance(result[0], Link)
            and result[0].id == 3
            and result[1].id == 2
        )

    async def test_get_latest_less_than_limit(self):
        self.populate_link(1)
        result = await self.link.get_latest(2)
        assert len(result) == 1

    async def test_get_latest_less_no_data(self):
        result = await self.link.get_latest(2)
        assert len(result) == 0
