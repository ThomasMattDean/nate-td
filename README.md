
# Word Counter

## Overview

This project consists of a web service which, when supplied with a url for a web page, will return the fifty most common words along with the number of occurrences of each word from the page.

## Prerequisites

The project can be run either with or without Docker (i.e directly on your machine). 

It is recommended to run the project with Docker. To do so you will need Docker installed (version 20.10.12 was used to create the project).

If you want to run the project without Docker you will need the following:

- python3.9.7
- pip
- pip-tools (which can be installed with `pip install pip-tools`)

## Installation & Usage

To run without Docker:

```sh
# build the Docker image
make docker-build
# run the api
make docker-run
# while docker is running, check the api is running by opening the following in a brower
http://0.0.0.0/health
# navigate to a url such as bbc news
http://0.0.0.0/urls?url=https://www.bbc.co.uk/news
# or a wikipedia article
http://0.0.0.0/urls?url=https://en.wikipedia.org/wiki/Python_(programming_language)
# or a new site
http://0.0.0.0/urls?url=https://techcrunch.com/
# view the docs
http://0.0.0.0/docs
```

To run without Docker:

```sh
# install requirements
make pip-sync
# run the api
make run
# pass a url
http://127.0.0.1:8000/urls?url=https://www.bbc.co.uk/news
# view the docs
http://127.0.0.1:8000/docs
```

## Testing

If you have followed the previous step tests can be run with Docker:

```sh
make docker-run-tests
```

Or without Docker:

```sh
make tests
```

## Details

- The [validators](https://validators.readthedocs.io/en/latest/) package is used to validate urls. Any urls not judged to be valid by the definition provided in these docs will return an error.
- Numbers such as '4' and phrases such as '4hr' are treated as words.
- Only ascii based text is currently supported, any non ascii characters will be removed and no error will be raised.
- The symbol '&' and the word 'and' have a combined score, returned as 'and'.
- The top fifty words are retrieved and are returned in descending order of occurrences.

## Scalability
- The [longest article of Wikipedia](https://en.wikipedia.org/wiki/Special:LongPages) has been used to give an upper bound for response times. These are consistently under 0.5ms for a page of this size.
- Basic load testing has been conduced up using Python's concurrency module


## TODO
- Split the `requirements.txt` and `requirement.in` files into a dev version and a production version.
- Extend to support non-ascii
- More rigorous load testing
- Investigate reliability of BeautifulSoup and Validators
- Find a more elegant solution to `remove_quotes`
- Expand testing of `processing` especially `test_process_url` - use a wider range of source docs