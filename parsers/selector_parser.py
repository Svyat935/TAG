from typing import Set


class SelectorParser:
    def __init__(self, selectors: Set[str] = None):
        self._selectors = selectors if selectors else set()

    @property
    def selectors(self):
        return self._selectors

    @selectors.setter
    def selectors(self, new_selectors):
        if not isinstance(new_selectors, (set, list, tuple)) or not all(
            [isinstance(class_, str) for class_ in new_selectors]
        ):
            raise ValueError("Selectors for parsing must be typing Set[str].")
        if not isinstance(new_selectors, set):
            new_selectors = set(new_selectors)
        self._selectors = new_selectors

    def parse_class_css(self, css_raw: str):
        output = dict()
        selector_name = None
        open_ = False

        string = ""
        for char in css_raw:
            if selector_name is None:
                if char in "#.," or open_ is True:
                    if char == "}":
                        open_ = False
                        string = ""
                    if char == ",":
                        string = ""
                    continue
                else:
                    if char == "{":
                        open_ = True
                        if string in self._selectors:
                            selector_name = string
                            string = ""
                            continue
            else:
                if char == "}":
                    open_ = False
                    output[selector_name] = string
                    selector_name = None
                    string = ""
                    continue

            string += char
        return output
