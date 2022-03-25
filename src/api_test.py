import logging

import pytest
from fastapi.testclient import TestClient
from pytest import fixture

import src.main
from src.main import app, is_url_valid

log = logging.getLogger(__name__)


@fixture
def client():
    return TestClient(app)


BBC_URL = "https://www.bbc.co.uk/news"
INVALID_URL = "https://www.bbc.co."


def test_health_check(client):
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"msg": "OK"}


def test_api(client, monkeypatch):
    mocked_words = [
        ["the", 118],
        ["ago", 72],
        ["in", 66],
        ["to", 57],
        ["hours", 50],
        ["for", 48],
        ["of", 42],
        ["europe", 42],
        ["ukraine", 37],
        ["it", 37],
    ]

    def mock_process_url(_):
        log.info("returning mocked result")
        return mocked_words

    monkeypatch.setattr(src.main, "process_url", mock_process_url)

    response = client.get(f"/urls?url={BBC_URL}")

    assert response.status_code == 200

    assert response.json() == {"data": mocked_words}


def test_api_invalid_input_error(client):
    response = client.get(f"/urls?url={INVALID_URL}")
    assert response.status_code == 422
    assert response.json() == {"detail": "The provided input does not appear to be a valid url"}


def test_api_internal_error(client, monkeypatch):
    def mock_process_url(_):
        log.info("returning mocked result")
        raise ValueError("mocked error")

    monkeypatch.setattr(src.main, "process_url", mock_process_url)

    response = client.get(f"/urls?url={BBC_URL}")
    assert response.status_code == 500
    assert response.json() == {"detail": "Internal error"}


params = [
    ("https://www.theguardian.com/uk", True),
    ("https://techcrunch.com/?guccounter=1&guce_referrer=aHR0cHM6Ly93d3c", True),
    ("https://techcrunch.c", False),
    ("https//techcrunch.com", False),
    ("techcrunch.com", False),
    ("1", False),
]


@pytest.mark.parametrize("url_text,is_valid", params)
def test_is_url_valid(url_text, is_valid):
    return is_url_valid(url_text) == is_valid
