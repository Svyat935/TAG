from sqlalchemy import Column, Integer, String

from db.db_connection import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=True)
    surname = Column(String, nullable=True)
    password = Column(String)
    email = Column(String)
    login = Column(String)

    def __repr__(self):
        return f"<User(id:{self.id}, login:{self.login}, email:{self.email}, password:{self.password})>"
