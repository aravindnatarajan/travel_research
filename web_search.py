from collections.abc import Sequence

from langchain_community.utilities import DuckDuckGoSearchAPIWrapper as ddg

import constants


class WebSearch:
    @property
    def links(self):
        return self._links
        
    def __init__(
        self,
        num_links: int = constants.NUM_LINKS,
    ):
        self._num_links = num_links
        self._links = set()

    def _search(
        self,
        web_query: str,
    ) -> Sequence[str]:
        return [
            result['link'] for result in ddg().results(
                web_query, self._num_links
            )
        ]

    def get_links(self, queries: list[str]):
        for query in queries:
            results = self._search(query)
            for result in results:
                self._links.add(result)
