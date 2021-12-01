from collections import defaultdict

from bs4 import BeautifulSoup
from typing import Set, List, Dict


class TagParser:
    def __init__(self, tags: Set[str] = None):
        self._tags = set(tags) if tags is not None else set()

    @property
    def tags(self) -> Set[str]:
        return self._tags

    @tags.setter
    def tags(self, new_tags: Set[str]) -> None:
        if not isinstance(new_tags, (set, list, tuple)) or not all(
            [isinstance(tag, str) for tag in new_tags]
        ):
            raise ValueError("Tags for parsing must be typing Set[str].")
        if not isinstance(new_tags, set):
            new_tags = set(new_tags)
        self._tags = new_tags

    def parse(self, html_raw: str) -> Dict[str, List[str]]:
        soup = BeautifulSoup(html_raw, "html.parser")
        finding_tags = soup.find_all(self._tags)

        output = defaultdict(list)
        for tag in finding_tags:
            output[tag.name].append(str(tag))

        return output if output else None
