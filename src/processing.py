"""Carries out all processing work i.e turns a url into a list of the most common words and their occurances"""

import logging
from collections import Counter
from string import ascii_letters, digits

import requests
from bs4 import BeautifulSoup  # type: ignore

log = logging.getLogger(__name__)

VALID_CHARACTERS = ascii_letters + digits + "".join(["-", "'", " "])
WORD_LIMIT = 50


def process_url(url: str) -> list[tuple[str, int]]:
    """Fetches the html from a specified url and returns a count of the most common words"""
    log.info(f'processing url "{url}"')
    content = retrieve_content(url)
    text = content_to_text(content)
    flatten_text = flatten(text)
    tidied_text = tidy_text(flatten_text)
    quotes_removed = remove_quotes(tidied_text)
    top_words = count_words(quotes_removed)
    return top_words


def retrieve_content(url: str) -> bytes:
    """Retrieves the html for a specified url."""
    log.info("retrieving webpage")
    return requests.get(url).content


def content_to_text(content: bytes) -> list[str]:
    """Converts html content in the form of bytes to list of strings using Beautiful Soup"""
    log.info("converting to text")
    # TODO - investigate how reliable Beautiful Soup is at parsing html
    soup = BeautifulSoup(content, "html.parser")
    strips = list(soup.stripped_strings)
    return strips


def flatten(text_as_list: list[str]) -> str:
    """Flattens a list of strings to a single string"""
    log.info("flattening list")
    # convert the list of lists into a single list
    as_single_list = [word for row in text_as_list for word in row.split(" ")]
    # strip leading and trailing blank spaces; remove words which are purely blank space
    stripped_words = [word.strip() for word in as_single_list if word]
    return " ".join(stripped_words)


def tidy_text(text_as_string: str) -> str:
    """Removes all characters which are not ascii or digits with the exception of apostrophes and hyphens; converts to lower case"""
    log.info("tidying text")
    text_as_string = text_as_string.lower()
    text_as_string = text_as_string.replace("&", "and")
    text_as_string = text_as_string.replace(" - ", " ")
    valid_text = [char for char in text_as_string if char in VALID_CHARACTERS]
    return "".join(valid_text)


def remove_quotes(text: str) -> str:
    """Removes single quotes but not apostrophes from text - relies on all other punctuation having been removed"""
    log.info("removing quotes")
    # TODO - find a more elegant solution, possibly using regex
    if text and text[0] == "'":
        text = text[1:]
    if text and text[-1] == "'":
        text = text[:-1]
    return text.replace(" '", " ").replace("' ", " ")


def count_words(text_as_string: str, n: int = WORD_LIMIT) -> list[tuple[str, int]]:
    """Provides a word count for the specified string"""
    log.info("generating word count")
    return Counter([word for word in text_as_string.split(" ") if word]).most_common(n)
