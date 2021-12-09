import time
from datetime import datetime, timedelta
from typing import List, Optional

import requests as requests

from db.db_connection import DBConnection
from models.html_template import HTMLTemplate
from models.site_settings import SiteSettings


class Daemon:
    def __init__(self):
        self.db_connection = DBConnection()

    def run(self):
        queue = self._create_queue()
        date_wait = queue[0]["date"].replace(microsecond=0)
        while True:
            now = datetime.now().replace(microsecond=0)
            if date_wait < now:
                print("Get sites")
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
