from pathlib import Path
from typing import Type

from db.db_connection import DBConnection


def test_create_db(setup: Type[DBConnection]):
    path = Path("test.db")
    assert path.is_file()
