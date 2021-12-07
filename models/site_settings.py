from sqlalchemy import Column, Integer, ForeignKey, JSON, String, Interval, DateTime
from sqlalchemy.orm import relationship

from db.db_connection import Base


class SiteSettings(Base):
    __tablename__ = "site_settings"

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    url = Column(String)
    search_settings = Column(JSON)
    search_interval = Column(Interval)
    start_date = Column(DateTime)

    user = relationship("User", back_populates="site_settings")

    def __repr__(self):
        return f"<SiteSettings(id:{self.id})>"
