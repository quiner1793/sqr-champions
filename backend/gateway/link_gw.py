from backend.gateway.db_gw import DatabaseGw
from backend.entity.link import Link


class LinkGw(DatabaseGw):

    async def add_link(self, link_data):
        self.cursor.execute('INSERT INTO Links (link, title, platform) '
                            'VALUES (?, ?, ?)',
                            (link_data.link,
                             link_data.title,
                             link_data.platform))
        self.con.commit()
        return self.cursor.lastrowid

    async def get_link_data_by_link(self, link: str):
        self.cursor.execute('SELECT * FROM Links WHERE link = ?', (link,))
        link_data = self.cursor.fetchone()
        if link_data is not None:
            return Link(id=link_data[0],
                        link=link_data[1],
                        title=link_data[2],
                        platform=link_data[3])
        return link_data

    async def get_link_data_by_link_id(self, link_id: int):
        self.cursor.execute('SELECT * FROM Links WHERE id = ?',
                            (int(link_id),))
        link_data = self.cursor.fetchone()
        if link_data is not None:
            return Link(id=link_data[0],
                        link=link_data[1],
                        title=link_data[2],
                        platform=link_data[3])
        return link_data

    async def get_links_by_query(self, query: str):
        self.cursor.execute("SELECT * FROM Links "
                            "WHERE title LIKE ? OR platform LIKE ?",
                            (f"%{query}%", f"%{query}%"))
        links_data = self.cursor.fetchall()
        result = []
        for link in links_data:
            result.append(Link(id=link[0],
                               link=link[1],
                               title=link[2],
                               platform=link[3]))
        return result

    async def get_latest(self, limit: int):
        self.cursor.execute('SELECT * FROM Links '
                            'ORDER BY id DESC LIMIT ?', (str(limit),))
        links_data = self.cursor.fetchall()
        result = []
        for link in links_data:
            result.append(Link(id=link[0],
                               link=link[1],
                               title=link[2],
                               platform=link[3]))
        return result
