from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship

from db.db_connection import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=True)
    surname = Column(String, nullable=True)
    email = Column(String)
    login = Column(String)
    password = Column(String)

    user_settings = relationship("UserSettings", back_populates="user")
    site_settings = relationship("SiteSettings", back_populates="user")

    def __repr__(self):
        return f"<User(id:{self.id}, login:{self.login}, email:{self.email}, password:{self.password})>"
