from sqlalchemy import Column, Integer, ForeignKey, JSON
from sqlalchemy.orm import relationship

from db.db_connection import Base


class UserSettings(Base):
    __tablename__ = "user_settings"

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'))
    settings = Column(JSON)

    user = relationship("User", back_populates="user_settings")

    def __repr__(self):
        return f"<UserSettings(id:{self.id})>"
