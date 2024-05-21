from typing import List
from base.parser import BaseParser

class BaseQueryReader:
    """
    Base class for reading queries from a file.
    """

    def __init__(self, file_path, lang="english"):
        self.file_path = file_path
        self.queries = self.get_queries()
        self.parser = BaseParser(lang)

        # Parse the queries
        self.parse_queries()

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
    
    def parse_queries(self, stem=True):
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