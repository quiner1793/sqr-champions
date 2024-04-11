import sqlite3


class DatabaseGw:
    def __init__(self, con: sqlite3.Connection):
        self.con = con
        self.cursor = self.con.cursor()

    async def create_tables(self) -> None:
        self.cursor.execute('''
                    CREATE TABLE IF NOT EXISTS Users (
                    id INTEGER PRIMARY KEY,
                    username TEXT NOT NULL UNIQUE,
                    password TEXT NOT NULL,
                    email TEXT NOT NULL UNIQUE
                    )
                    ''')

        self.cursor.execute('''
                        CREATE TABLE IF NOT EXISTS Links (
                        id INTEGER PRIMARY KEY,
                        link TEXT NOT NULL UNIQUE,
                        title TEXT NOT NULL,
                        platform TEXT NOT NULL
                        )
                        ''')

        self.cursor.execute('''
                    CREATE TABLE IF NOT EXISTS Feedback (
                    id INTEGER PRIMARY KEY,
                    user_id INTEGER NOT NULL,
                    link_id INTEGER NOT NULL,
                    comment TEXT NOT NULL,
                    date DATETIME NOT NULL,
                    FOREIGN KEY(user_id) REFERENCES Users(id),
                    FOREIGN KEY(link_id) REFERENCES Links(id)
                    )
                    ''')
        self.con.commit()
