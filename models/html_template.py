from sqlalchemy import Column, Integer, String, DateTime

from db.db_connection import Base


class HTMLTemplate(Base):
    __tablename__ = "html_templates"

    id = Column(Integer, primary_key=True)
    url = Column(String)
    raw_html = Column(String)
    raw_css = Column(String)
    date = Column(DateTime)

    def __repr__(self):
        return f"<HTMLTemplate(id:{self.id})>"
