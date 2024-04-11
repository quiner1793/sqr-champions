from backend.gateway.db_gw import DatabaseGw
from backend.entity.user import User


class UserGw(DatabaseGw):
    async def add_user(self, user_data):
        self.cursor.execute('INSERT INTO Users (username, password, email) '
                            'VALUES (?, ?, ?)',
                            (user_data.username,
                             user_data.password,
                             user_data.email))

        self.con.commit()
        return self.cursor.lastrowid

    async def get_user(self, user_data):
        self.cursor.execute('SELECT * FROM Users '
                            'WHERE username = ? AND password = ?',
                            (user_data.username, user_data.password))
        user = self.cursor.fetchone()
        if user is not None:
            user = User(id=user[0],
                        username=user[1],
                        password=user[2],
                        email=user[3])

        return user

    async def get_user_by_username(self, username: str):
        self.cursor.execute('SELECT * FROM Users '
                            'WHERE username = ?', (username,))
        user = self.cursor.fetchone()
        if user is None:
            return user
        return User(id=user[0],
                    username=user[1],
                    password=user[2],
                    email=user[3])

    async def get_username_by_id(self, user_id: int):
        self.cursor.execute('SELECT username FROM Users '
                            'WHERE id = ?', (str(user_id),))
        username = self.cursor.fetchone()

        return username[0]
