from typing import Type

from db.db_connection import DBConnection


class DBInstance:
    def __init__(self, db: Type[DBConnection]):
        self.db = db()
