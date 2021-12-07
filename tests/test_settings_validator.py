import pytest

from validators.settings_validator import SettingsValidator


def test_validate_settings_positive(site_settings):
    settings = SettingsValidator.validate_site_settings(site_settings)

    assert settings


def test_validate_settings_empty():
    settings = {}
    with pytest.raises(ValueError) as info1:
        SettingsValidator.validate_site_settings(settings)
    settings = {"html_tags": ["meta", "link"]}
    with pytest.raises(ValueError) as info2:
        SettingsValidator.validate_site_settings(settings)
    settings = {"html_tags": ["meta", "link"], "css_tags": ["button"]}
    with pytest.raises(ValueError) as info3:
        SettingsValidator.validate_site_settings(settings)
    settings = {
        "html_tags": ["meta", "link"],
        "css_tags": ["button"],
        "interval": "1 day",
    }
    with pytest.raises(ValueError) as info4:
        SettingsValidator.validate_site_settings(settings)

    assert info4 and info3 and info2 and info1


def test_validate_settings_regex():
    settings = {"html_tags": [], "css_tags": [], "interval": "1 TestDay", "url": "test"}

    with pytest.raises(ValueError) as info:
        SettingsValidator.validate_site_settings(settings)

    assert (
        info.value.args[0] == "Field 'interval' must be '1 day', '1 hour', '1 minutes'"
    )


def test_validate_values_negative():
    settings = {
        "html_tags": ["test", 1, 2, 3],
        "css_tags": ["test", 1, 2, 3],
        "interval": "1 day",
        "url": "test",
    }

    with pytest.raises(ValueError) as info1:
        SettingsValidator.validate_site_settings(settings)

    settings["html_tags"] = ["test"]
    with pytest.raises(ValueError) as info2:
        SettingsValidator.validate_site_settings(settings)

    assert (
        info1.value.args[0] == "Tags of HTML must be string"
        and info2.value.args[0] == "Tags of CSS must be string"
    )
