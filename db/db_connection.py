from contextlib import contextmanager

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base, Session

DEFAULT_URL = "sqlite:///db/database.db"

Base = declarative_base()


class DBConnection:
    def __init__(self, url: str = DEFAULT_URL):
        self._url = url
        self._engine = create_engine(url)

        Base.metadata.create_all(self._engine)

    @property
    def url(self):
        return self._url

    @property
    def engine(self):
        return self._engine

    @contextmanager
    def create_connection(self) -> Session:
        session = sessionmaker(bind=self._engine, autocommit=True, autoflush=True)()
        try:
            yield session
        finally:
            session.close()
