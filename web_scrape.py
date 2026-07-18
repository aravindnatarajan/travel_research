import requests
from collections.abc import Mapping

from bs4 import BeautifulSoup

import constants

class WebScrape:
    '''Scrape data from a list of URLs.

    Attributes:
      documents: A dictionary of URLs mapped to text.
    '''
    def __init__(
        self,
        timeout: int = constants.TIMEOUT,
        min_length: int = constants.MIN_LENGTH,
    ):
        self._timeout = timeout
        self._min_length = min_length
        self._documents: Mapping[str, str] = {}
        self._headers = {
            'User-Agent': (
                'Mozilla/5.0 (Windows NT 10.0; Win64; x64) '
                'AppleWebKit/537.36 (KHTML, like Gecko) '
                'Chrome/124.0.0.0 Safari/537.36'
            ),
            'Accept-Language': 'en-US,en;q=0.9',
        }
        

    @property
    def documents(self):
        return self._documents

    def _not_empty(self, doc) -> bool:
        return len(doc.split()) >= self._min_length
    
    def _scrape_link(self, url: str) -> str:
        '''Scrape a webpage.'''
        try:
            response = requests.get(url, headers=self._headers, timeout=self._timeout)
            if response.status_code == 200:
                return BeautifulSoup(
                    response.text, 'html.parser'
                ).get_text(separator=' ', strip=True)
            else:
                return ''
        except Exception as e:
            return ''

    def scrape(self, links: list[str]):
        '''Collect data from a list of URLs.

        Args:
          links: The list of URLs to scrape.
        '''
        for link in links:
            text = self._scrape_link(link)
            if self._not_empty(text):
                self._documents[link] = text
