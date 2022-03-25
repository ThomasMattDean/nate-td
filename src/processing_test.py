"""
Unit tests for the processing, all except the final one test one specific function. 

The final tests mocks the retrieval of content and tests everything else
"""

from dataclasses import dataclass

import pytest
import requests

import src.processing
from src.tests_assets.html import HTML_FORM, HTML_MARKERS, HTML_PARAGRAPH, HTMLPAGE, TWITTER, W3_SCHOOLS, WIKIPEDIA  # type: ignore
from src.processing import (
    content_to_text,
    count_words,
    flatten,
    process_url,
    remove_quotes,
    retrieve_content,
    tidy_text,
)


def test_retrieve_content(monkeypatch):
    @dataclass
    class MockHtml:
        content: str = "some content"

    def mock_get(_):
        return MockHtml()

    monkeypatch.setattr(requests, "get", mock_get)

    assert retrieve_content("some url") == "some content"


content_to_text_params = [
    (HTML_FORM, ["Text Input:", "Radio Button Choice", "Choice 1", "Choice 2"], "form"),
    (HTML_PARAGRAPH, ["Pellentesque habitant morbi tristique."], "paragraph"),
]


@pytest.mark.parametrize("content,output,_", content_to_text_params, ids=[row[-1] for row in content_to_text_params])
def test_content_to_text(content, output, _):
    assert content_to_text(content) == output


def test_content_to_text_full_page():
    result = content_to_text(HTMLPAGE)
    text = "".join(result)
    for marker in HTML_MARKERS:
        assert marker not in text


def test_flatten():
    strings = ["  the cat", "sat   on", "" "rhe mat", " "]
    assert flatten(strings) == "the cat sat on rhe mat"
    assert flatten([]) == ""


def test_remove_quotes():
    string_with_quotes = "first 'tell' the audience what you're going to say 'say it' and then"
    assert remove_quotes(string_with_quotes) == "first tell the audience what you're going to say say it and then"

    string_with_quotes_at_ends = "'Tell' the audience what you're going to say 'say it' and then 'tell'"
    assert (
        remove_quotes(string_with_quotes_at_ends) == "Tell the audience what you're going to say say it and then tell"
    )
    assert remove_quotes("") == ""


def test_tidy_text():
    text = "tell the-audience, what *you're* going to say. (Say it) & Then tell them what you've said."
    assert tidy_text(text) == "tell the-audience what you're going to say say it and then tell them what you've said"
    assert tidy_text("") == ""


def test_count_words():
    word_list = "tell the-audience what you're going to say say it and then tell them what you've said"
    assert count_words(word_list, 4) == [("tell", 2), ("what", 2), ("say", 2), ("the-audience", 1)]
    assert count_words("") == []


# mypy ignore statements are necessary as pytest and mypy do not fully get on
process_url_params = [
    (W3_SCHOOLS, [("code", 2), ("game", 1), ("tutorials", 1)], "W3 Schools"),  # type: ignore
    (WIKIPEDIA, [("wikipedia", 1), ("the", 1), ("free", 1)], "Wikipedia"),  # type: ignore
    (TWITTER, [], "Twitter"),
]


@pytest.mark.parametrize("html,result,_", process_url_params, ids=[p[2] for p in process_url_params])
def test_process_url(html, result, _, monkeypatch):
    def mock_retrieve_content(_):
        return html

    monkeypatch.setattr(src.processing, "retrieve_content", mock_retrieve_content)

    assert process_url("")[:3] == result
