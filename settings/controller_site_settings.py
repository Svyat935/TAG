from typing import List

from db.db_connection import DBConnection
from models.html_template import HTMLTemplate
from models.site_settings import SiteSettings
from models.user import User


class ControllerSiteSettings:
    def __init__(self, db_connection: DBConnection = DBConnection()):
        self._db = db_connection

    def create_site_settings(self, settings: SiteSettings) -> None:
        with self._db.create_connection() as db:
            old_settings: SiteSettings = (
                db.query(SiteSettings).filter(SiteSettings.user_id == settings.user_id).first()
            )
            if old_settings:
                old_settings.search_settings = settings.search_settings
                old_settings.url = settings.url
                old_settings.search_interval = settings.search_interval
                old_settings.current_date = old_settings.current_date
                db.add(old_settings)
            else:
                db.add(settings)
            db.commit()

    def check_site_settings(self, settings: SiteSettings) -> bool:
        with self._db.create_connection() as db:
            settings = (
                db.query(SiteSettings).filter(SiteSettings.id == settings.id).first()
            )
            return bool(settings)

    def get_user_site_settings(self, user: User) -> SiteSettings:
        with self._db.create_connection() as db:
            settings = (
                db.query(SiteSettings).filter(SiteSettings.user_id == user.id).first()
            )
            return settings

    def get_html_templates_for_settings(self, settings: SiteSettings) -> List[HTMLTemplate]:
        url = settings.url
        with self._db.create_connection() as db:
            html_templates = db.query(HTMLTemplate).filter(HTMLTemplate.url == url).all()
            return html_templates
