import asyncio
import datetime
import sqlite3
from unittest import IsolatedAsyncioTestCase

from backend.entity.feedback import Feedback
from backend.gateway.db_gw import DatabaseGw
from backend.gateway.feedback_gw import FEEDBACK_DATETIME_FORMAT, FeedbackGw

# from aiounittest import async_test

# import pytest


class TestFeedback(IsolatedAsyncioTestCase):
    def populate_feedback(
        self,
        limit: int,
        date: str,
        inc_link_id: bool = True,
        inc_user_id: bool = True,
        default_link_id: int = None,
    ):
        for i in range(1, limit):
            self.db.cursor.execute(
                "INSERT INTO Feedback "
                "(user_id, link_id, comment, date) "
                "VALUES (?, ?, ?, datetime(?))",
                (
                    self.feedback_data.user_id + (i if inc_user_id else 0),
                    (
                        self.feedback_data.link_id + (i if inc_link_id else 0)
                        if default_link_id is None
                        else default_link_id
                    ),
                    f"{self.feedback_data.comment}_{i}",
                    date,
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
        self.feedback = FeedbackGw(self.connection)
        self.feedback_data = Feedback(
            user_id=1, link_id=1, comment="Testing comment")

    def tearDown(self) -> None:
        del self.db
        del self.connection

    async def test_add_feedback(self):
        await self.feedback.add_feedback(self.feedback_data)
        self.db.cursor.execute(
            "SELECT * FROM Feedback " "WHERE link_id = ?",
            (str(self.feedback_data.link_id),),
        )
        result = self.db.cursor.fetchall()
        assert (
            len(result) == 1
            and result[0][0] == 1
            and result[0][1] == self.feedback_data.user_id
            and result[0][2] == self.feedback_data.link_id
            and result[0][3] == self.feedback_data.comment
            and datetime.datetime.strptime(
                result[0][4], FEEDBACK_DATETIME_FORMAT)
            < datetime.datetime.now()
        )

    async def test_get_feedback_by_id(self):
        date = await self.feedback.add_feedback(self.feedback_data)
        result = await self.feedback.get_feedback_by_id(1)
        assert (
            isinstance(result, Feedback)
            and result.id == 1
            and result.user_id == self.feedback_data.user_id
            and result.link_id == self.feedback_data.link_id
            and result.comment == self.feedback_data.comment
            and result.date == date
        )

    async def test_get_not_existing_feedback(self):
        result = await self.feedback.get_feedback_by_id(1)
        assert result is None

    async def test_get_feedback_list(self):
        date = datetime.datetime(2024, 4, 25, 10, 0, 0).strftime(
            FEEDBACK_DATETIME_FORMAT
        )
        self.populate_feedback(4, date, inc_link_id=False, inc_user_id=False)
        self.populate_feedback(1, date, default_link_id=3)
        result = await self.feedback.get_feedback_list(
            self.feedback_data.link_id)
        for i in range(3):
            assert (
                len(result) == 3
                and isinstance(result[i], Feedback)
                and result[i].link_id == self.feedback_data.link_id
            )

    async def test_get_empty_feedback_list(self):
        date = datetime.datetime(2024, 4, 25, 10, 0, 0).strftime(
            FEEDBACK_DATETIME_FORMAT
        )
        self.populate_feedback(limit=3, date=date)
        result = await self.feedback.get_feedback_list(
            self.feedback_data.link_id)
        assert len(result) == 0

    async def test_get_latest_feedback(self):
        date = datetime.datetime(2024, 4, 25, 10, 0, 0).strftime(
            FEEDBACK_DATETIME_FORMAT
        )
        self.populate_feedback(limit=4, date=date)
        result = await self.feedback.get_latest_feedback(limit=2)
        assert len(result) == 2
        for i in range(2):
            assert (
                isinstance(result[i], Feedback)
                and result[i].id == 3 - i
                and result[i].user_id == 4 - i
                and result[i].link_id == 4 - i
                and result[i].comment == f"{self.feedback_data.comment}_{3-i}"
                and result[i].date == date
            )

    async def test_get_latest_feedback_zero_limit(self):
        result = await self.feedback.get_latest_feedback(limit=0)
        assert len(result) == 0

    async def test_get_empty_latest_feedback(self):
        result = await self.feedback.get_latest_feedback(limit=2)
        assert len(result) == 0

    async def test_get_first_feedback(self):
        date = datetime.datetime(2024, 4, 25, 10, 0, 0).strftime(
            FEEDBACK_DATETIME_FORMAT
        )
        self.populate_feedback(limit=4, date=date, inc_link_id=False)
        result = await self.feedback.get_first_feedback(
            self.feedback_data.link_id)
        assert (
            isinstance(result, Feedback)
            and result.link_id == self.feedback_data.link_id
            and result.id == 1
            and result.user_id == self.feedback_data.user_id + 1
        )

    async def test_get_first_feedback_not_existing_link(self):
        date = datetime.datetime(2024, 4, 25, 10, 0, 0).strftime(
            FEEDBACK_DATETIME_FORMAT
        )
        self.populate_feedback(limit=4, date=date)
        result = await self.feedback.get_first_feedback(
            self.feedback_data.link_id)
        assert result is None
