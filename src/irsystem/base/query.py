from dataclasses import dataclass
from typing import Any, Dict, List
from base.parser import BaseParser


@dataclass
class Query:
    """
    `Query` contains all information regarding a query, including
    the query statement, tokens, term frequencies, and term weights.
    """

    id: int
    content: str
    tokens: List[str]
    term_freqs: Dict[str, float]
    term_weights: Dict[str, float]
    similarities: Dict[int, float]

    @staticmethod
    def from_raw(raw_query: Dict[str, Any]) -> "Query":
        """
        Converts raw query represented by a dictionary into
        its corresponding `Query` object.

        Args:
            `raw_query`: raw representation of the query

        Returns:
            A `Query` equivalent for the raw query dictionary.
        """

        return Query(
            raw_query["query_id"],
            raw_query["query"],
            raw_query["tokens"],
            {},
            {},
            {}
        )


class BaseQueryReader:
    """
    Base class for reading queries from a file.
    """

    def __init__(self, file_path, lang="english", stem: bool = True):
        self.file_path = file_path
        self.queries = self.get_queries()
        self.parser = BaseParser(lang)

        # Parse the queries
        self.parse_queries(stem)

    def get_queries(self) -> List[dict]:
        """
        Parse the file into a list of queries.

        Returns:
            list: A list of dictionaries, where each dictionary represents a query.

        [
            {
                'query_id': 3,
                'query': 'What is information science?  Give definitions where possible.',
            }
        ]
        """
        raise NotImplementedError

    def parse_queries(self, stem: bool = True):
        """
        Parse the queries into a list of dictionaries.

        - Tokenization
        - Removing stopwords

        Args:
            stem (bool): Whether to stem the tokens.
        """

        # Tokenization
        for query in self.queries:
            query["tokens"] = self.parser.parse(query["query"], stem)

    def to_query_list(self) -> List[Query]:
        """
        Extracts parsed raw queries into a list of `Query`.

        Returns:
            A list of `Query`.
        """
        return [Query.from_raw(raw_query) for raw_query in self.queries]
