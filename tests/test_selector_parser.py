import pytest

from parsers.selector_parser import SelectorParser


def test_save_selectors_positive():
    selectors = {"btn", "test", "input"}
    selector_parser = SelectorParser(selectors)

    before_selectors = selector_parser.selectors
    new_selectors = ["body", "test", "input"]
    selector_parser.selectors = new_selectors
    after_selectors = selector_parser.selectors

    assert (
        before_selectors == selectors
        and after_selectors == set(new_selectors)
        and after_selectors != before_selectors
    )


def test_save_selectors_negative():
    selector_parser = SelectorParser()
    with pytest.raises(ValueError) as info1:
        selector_parser.selectors = {"head": 1, "div": 1, "span": 1}

    with pytest.raises(ValueError) as info2:
        selector_parser.selectors = {"head", "div", "span", 123, b"333"}

    assert (
        info1.value.args[0]
        == info2.value.args[0]
        == "Selectors for parsing must be typing Set[str]."
    )


def test_css_parser(row_css):
    selector_parser = SelectorParser({"btn", "btn:hover", "tm-labeled-checkbox__input"})
    selectors = selector_parser.parse_class_css(row_css)

    assert selectors == {
        "btn": "border:1px solid transparent;border-radius:3px;font-size:.8125rem;align-self:self-start;transition:all .3s",
        "btn:hover": "outline:none;transition:all .3s",
        "tm-labeled-checkbox__input": "margin:1px 8px 0 0",
    }
