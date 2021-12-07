from typing import List

from db.db_connection import DBConnection
from models.site_settings import SiteSettings
from models.user import User


class ControllerSiteSettings:
    def __init__(self, db_connection: DBConnection = DBConnection()):
        self._db = db_connection

    def create_site_settings(self, settings: SiteSettings) -> None:
        with self._db.create_connection() as db:
            db.add(settings)
            db.commit()

    def check_site_settings(self, settings: SiteSettings) -> bool:
        with self._db.create_connection() as db:
            settings = (
                db.query(SiteSettings).filter(SiteSettings.id == settings.id).first()
            )
            return bool(settings)

    def get_user_site_settings(self, user: User) -> List[SiteSettings]:
        with self._db.create_connection() as db:
            settings = (
                db.query(SiteSettings).filter(SiteSettings.user_id == user.id).all()
            )
            return settings
