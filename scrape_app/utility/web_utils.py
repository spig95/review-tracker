import requests
from bs4 import BeautifulSoup

from scrape_app.utility.logger import log


def get_soup(url, custom_headers=None) -> BeautifulSoup:
    return BeautifulSoup(get_html_content(url, custom_headers), 'html.parser')


def get_html_content(url, custom_headers=None):
    """Interface to requests.get with a custom header.

    :param url: url from where to get html content
    :param custom_headers: dictionary with custom headers, can be None

    .. note:: use this function instead of requests.get(), this should be safer to potential blocks by browsers.
    """
    log.debug(f"Getting html content for {url}")
    if custom_headers is None:
        html = requests.get(url=url)
    else:
        html = requests.get(url=url, headers=custom_headers)
    log.debug(f"Got html content!")
    return html.content
