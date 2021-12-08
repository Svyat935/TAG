import re
from typing import Dict, Union, List


class SettingsValidator:
    @staticmethod
    def validate_site_settings(settings: Dict[str, Union[str, List[str]]]):
        if settings.get("html_tags") is None:
            raise ValueError("Settings must have field 'html_tags'")
        if settings.get("css_tags") is None:
            raise ValueError("Settings must have field 'css_tags'")
        if settings.get("interval") is None:
            raise ValueError("Settings must have field 'interval'")
        if settings.get("url") is None:
            raise ValueError("Settings must have field 'url'")

        if not re.fullmatch(r"1\s(day|hour|minute)", settings["interval"]):
            raise ValueError("Field 'interval' must be '1 day', '1 hour', '1 minute'")

        if not all([isinstance(tag, str) for tag in settings["html_tags"]]):
            raise ValueError("Tags of HTML must be string")
        if not all([isinstance(tag, str) for tag in settings["css_tags"]]):
            raise ValueError("Tags of CSS must be string")

        return settings

    @staticmethod
    def validate_user_settings():
        pass
