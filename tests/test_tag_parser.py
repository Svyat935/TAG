import pytest

from parsers.tag_parser import TagParser


def test_save_tags_positive():
    tags = {"div", "head", "meta"}
    tag_parser = TagParser(tags)

    before_tags = tag_parser.tags
    new_tags = [
        "head",
        "iframe",
        "span",
        "span",
        "span",
        "iframe",
    ]
    tag_parser.tags = new_tags
    after_tags = tag_parser.tags

    assert (
        before_tags == tags
        and after_tags == set(new_tags)
        and after_tags != before_tags
    )


def test_save_tags_negative():
    tag_parser = TagParser()
    with pytest.raises(ValueError) as info1:
        tag_parser.tags = {"head": 1, "div": 1, "span": 1}

    with pytest.raises(ValueError) as info2:
        tag_parser.tags = {"head", "div", "span", 123, b"333"}

    assert (
        info1.value.args[0]
        == info2.value.args[0]
        == "Tags for parsing must be typing Set[str]."
    )


def test_parse_tags(row_html):
    tag_parser = TagParser({"meta", "h1", "test_tag"})

    tags = tag_parser.parse(row_html)
    assert tags == {
        "h1": [
            '<h1>Quickstart<a class="headerlink" href="#quickstart" '
            'title="Permalink to this headline">В¶</a></h1>'
        ],
        "meta": [
            '<meta charset="utf-8"/>',
            '<meta content="width=device-width, initial-scale=1.0" '
            'name="viewport"/>',
            '<meta content="width=device-width, initial-scale=1" ' 'name="viewport"/>',
        ],
    }


def test_parse_unexisting_tags(row_html):
    tag_parser = TagParser({"test1", "test2", "test3"})

    tags = tag_parser.parse(row_html)
    assert not tags
