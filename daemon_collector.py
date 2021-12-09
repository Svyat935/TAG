import time
from datetime import datetime, timedelta
from typing import List, Optional

import requests as requests

from db.db_connection import DBConnection
from models.html_template import HTMLTemplate
from models.site_settings import SiteSettings
from validators.settings_validator import SettingsValidator
from settings.controller_site_settings import ControllerSiteSettings
from models.user import User

from os import listdir
from os.path import isfile, join
import json
from pathlib import Path


class Daemon:
    def __init__(self):
        self.db_connection = DBConnection()
        self.modules = 'modules'

    def run(self):
        queue = self._create_queue()
        date_wait = queue[0]["date"].replace(microsecond=0)
        while True:
            now = datetime.now().replace(microsecond=0)
            if date_wait < now:
                print("Get sites and modules")
                try:
                    addictional_modules = [f for f in listdir(self.modules) if isfile(join(self.modules, f))]
                    for i in addictional_modules:
                        with open(self.modules + "/" + i, 'r') as file:
                            settings = json.load(file)
                            SettingsValidator.validate_site_settings(settings)
                            interval = settings["interval"]
                            if interval == "1 day":
                                interval = timedelta(days=1)
                            elif interval == "1 hour":
                                interval = timedelta(hours=1)
                            else:
                                interval = timedelta(minutes=1)

                            with self.db_connection.create_connection() as conn:
                                user_id = conn.query(User).filter(User.login == settings["username"]).first()

                            site_settings = SiteSettings(
                                user_id=user_id.id,
                                url=settings["url"],
                                search_settings=json.dumps(settings),
                                search_interval=interval,
                                current_date=datetime.now(),
                            )
                            ControllerSiteSettings().create_site_settings(site_settings)
                        Path(self.modules + "/" + i).rename(self.modules + "/executed/" + i)

                except Exception as e:
                    print("{0}".format(e))

                while True:
                    site = queue[0]
                    if site["date"] < now:
                        site = queue.pop(0)
                        url = site["url"]
                        html = self._get_site(url)
                        if html:
                            self._create_html_template(url, html, datetime.now())
                        site["date"] += site["interval"] + timedelta(seconds=1)
                        queue.append(site)
                    else:
                        break

                queue = self._create_queue()
                queue = sorted(queue, key=lambda obj: obj["date"])
                date_wait = queue[0]["date"].replace(microsecond=0)
            else:
                sleep_length = date_wait - now
                sleep_length = sleep_length.seconds
                if sleep_length == 0:
                    sleep_length = 1
                print(f"Sleep: {sleep_length}. Now: {now}. Wait: {date_wait}")
                time.sleep(sleep_length)


    def _create_html_template(
        self, url: str, raw_html: str, date: datetime
    ) -> None:
        with self.db_connection.create_connection() as conn:
            html_template = HTMLTemplate(
                url=url,
                raw_html=raw_html,
                date=date,
            )
            conn.add(html_template)
            conn.commit()

    def _get_site(self, url) -> Optional[str]:
        try:
            data = requests.get(url)
        except ConnectionError:
            return None
        return str(data.content)

    def _create_queue(self):
        sites: List[SiteSettings] = self._get_all_sites()
        queue = []
        for site in sites:
            date = site.current_date
            while date < datetime.now():
                date += site.search_interval

            queue.append(
                {"date": date, "interval": site.search_interval, "url": site.url}
            )
        if queue:
            queue = sorted(queue, key=lambda obj: obj["date"])
            return queue
        return None

    def _get_all_sites(self) -> List[SiteSettings]:
        with self.db_connection.create_connection() as conn:
            sites: List[SiteSettings] = conn.query(SiteSettings).all()
            return sites


if __name__ == "__main__":
    daemon = Daemon()
    daemon.run()
