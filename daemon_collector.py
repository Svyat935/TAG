import time
from datetime import datetime
from typing import List

import requests as requests

from db.db_connection import DBConnection
from models.html_template import HTMLTemplate
from models.site_settings import SiteSettings


class Daemon:
    def __init__(self):
        self.db_connection = DBConnection()

    def run(self):
        queue = self._create_queue()
        date_wait = queue[0]["date"]
        while True:
            if date_wait <= datetime.now():
                while True:
                    if not queue:
                        break
                    site = queue[0]
                    if site["date"] <= datetime.now():
                        url = site["url"]
                        html = self._get_site(url)
                        if html:
                            with self.db_connection.create_connection() as conn:
                                html_template = HTMLTemplate(
                                    url=url,
                                    raw_html=html,
                                    date=datetime.now(),
                                )
                                conn.add(html_template)
                                conn.commit()
                        queue.append(queue.pop(0))
                    else:
                        break
            else:
                sleep_length = datetime.now() - date_wait
                time.sleep(sleep_length)

    def _get_site(self, url):
        try:
            data = requests.get(url)
        except ConnectionError:
            return None
        return data.content

    def _create_queue(self):
        sites: List[SiteSettings] = self._get_all_sites()
        queue = []
        for site in sites:
            date = (
                site.start_date
                if datetime.now() < site.start_date
                else site.start_date + site.search_interval
            )
            queue.append({"date": date, "url": site.url})
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
