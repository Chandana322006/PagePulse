import pytest
from parser import parse_page


# Happy path
def test_parse_page_success():

    data = {
        "title": "My Website",
        "links": [
            "home",
            "about"
        ]
    }

    result = parse_page(data)

    assert result["title"] == "My Website"
    assert result["links"] == 2


# Failure case 1
def test_parse_page_missing_title():

    data = {
        "links": []
    }

    with pytest.raises(ValueError):
        parse_page(data)


# Failure case 2
def test_parse_page_invalid_input():

    data = None

    with pytest.raises(AttributeError):
        parse_page(data)