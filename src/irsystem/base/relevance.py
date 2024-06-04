from typing import Any, Dict, List


class BaseRelevanceReader:
    """
    Base class for reading relevance judgments from a file.
    """

    def __init__(self, file_path):
        self.file_path = file_path
        self.relevances = self.get_relevances()

    def get_relevances(self) -> List[dict]:
        """
        Parse the file into a list of queries paired with its relevant documents.

        Returns:
            list: A list of dictionaries, where each dictionary represents a query's relevance judgment.

        [
            {
                'query_id': 1,
                'docs_id': [17, 46, 62],
            }
        ]
        """
        raise NotImplementedError

    def convert_to_dict(self):
        """
        Convert list to dictionary for fast lookups.

        Returns:
            dict: A dictionary where the query_id is the key 
                  and the list of relevant documents is the value.
        """
        relevances_dict = {}
        for relevance in self.relevances:
            relevances_dict[relevance["query_id"]] = relevance["docs_id"]
        return relevances_dict
