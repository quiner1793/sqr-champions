import asyncio
import copy
import datetime
import sqlite3

import pytest

from backend.__main__ import app
from backend.gateway.db_gw import DatabaseGw
from backend.gateway.feedback_gw import FEEDBACK_DATETIME_FORMAT

link = {
    "link": "https://stackoverflow.com/questions/23033939",
    "title": "How to fix bug",
    "platform": "stackoverflow",
    "comment": "Very amazing comment",
}
registration = {
    "username": "username",
    "email": "a@mail.ru",
    "password": "testpassword",
}
test_user = {
    "username": "test_user",
    "password": "test_password",
    "email": "test_email@mail.ru",
}
test_link = {
    "link": "https://github.com/test/test_project",
    "title": "How to fix test",
    "platform": "github",
    "comment": "Testing comment",
}
test_feedback = {
    "user_id": 1,
    "link_id": 1,
    "comment": "Testing comment",
    "date": datetime.datetime(
        2024, 4, 25, 10, 0, 0).strftime(FEEDBACK_DATETIME_FORMAT),
}


def await_func(func) -> None:
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(None)
    loop.run_until_complete(func)


def populate_tables(db):
    db.cursor.execute(
        "INSERT INTO Users (username, password, email) " "VALUES (?, ?, ?)",
        (test_user["username"], test_user["password"], test_user["email"]),
    )
    db.con.commit()

    db.cursor.execute(
        "INSERT INTO Links (link, title, platform) " "VALUES (?, ?, ?)",
        (test_link["link"], test_link["title"], test_link["platform"]),
    )
    db.con.commit()

    db.cursor.execute(
        "INSERT INTO Feedback "
        "(user_id, link_id, comment, date) "
        "VALUES (?, ?, ?, datetime(?))",
        (
            test_feedback["user_id"],
            test_feedback["link_id"],
            test_feedback["comment"],
            test_feedback["date"],
        ),
    )
    db.con.commit()


@pytest.fixture
def test_app():
    connection = sqlite3.connect(":memory:")
    db = DatabaseGw(connection)
    await_func(db.create_tables())
    populate_tables(db)
    app.state.db = connection
    yield app
    del db
    del connection


@pytest.fixture
def registration_data():
    return copy.copy(registration)


@pytest.fixture
def test_user_data():
    return copy.copy(test_user)


@pytest.fixture
def test_link_data():
    return copy.copy(test_link)


@pytest.fixture
def test_feedback_data():
    return copy.copy(test_feedback)


@pytest.fixture
def link_data():
    return copy.copy(link)
