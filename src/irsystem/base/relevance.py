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

