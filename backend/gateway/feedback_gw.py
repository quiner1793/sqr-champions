from datetime import datetime
from zoneinfo import ZoneInfo

from backend.gateway.db_gw import DatabaseGw
from backend.entity.feedback import Feedback

FORMAT = "%Y-%m-%d %H:%M:%S"


class FeedbackGw(DatabaseGw):
    async def add_feedback(self, feedback_data):
        self.cursor.execute('INSERT INTO Feedback '
                            '(user_id, link_id, comment, date) '
                            'VALUES (?, ?, ?, datetime(?))',
                            (feedback_data.user_id,
                             feedback_data.link_id,
                             feedback_data.comment,
                             datetime.now(tz=ZoneInfo('Europe/Moscow')).strftime(FORMAT)))  # noqa: E501
        self.con.commit()

    async def get_feedback_by_id(self, feedback_id: int):
        self.cursor.execute('SELECT * FROM Feedback '
                            'WHERE id = ?', (str(feedback_id),))
        feedback = self.cursor.fetchone()
        if feedback is None:
            return feedback
        return Feedback(id=feedback[0],
                        user_id=feedback[1],
                        link_id=feedback[2],
                        comment=feedback[3],
                        date=feedback[4])

    async def get_feedback_list(self, link_id: int):
        self.cursor.execute('SELECT * FROM Feedback '
                            'WHERE link_id = ?', (str(link_id),))
        result = self.cursor.fetchall()
        feedback_list = []
        for feedback in result:
            feedback_list.append(Feedback(id=feedback[0],
                                          user_id=feedback[1],
                                          link_id=feedback[2],
                                          comment=feedback[3],
                                          date=feedback[4]))
        return feedback_list
