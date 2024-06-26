import math
import nltk
import pandas as pd
from collections import defaultdict
from typing import Dict, List
from base.parser import BaseParser


class BaseDocReader:
    """
    Base class for document readers.

    Attributes:
        file_path (str): The path to the file to read.
        docs (list): A list of dictionaries, where each dictionary represents a document.
        word_set (set): A set of unique words in the documents.
    """
    stemmer = nltk.PorterStemmer()

    def __init__(self, file_path, lang="english", stem: bool = True):
        self.file_path = file_path
        self.docs = self.get_docs()
        self.tf_table = None
        self.wc_table = defaultdict(int)
        self.word_set = set()
        self.parser = BaseParser(lang)

        # Parse the documents
        self.parse_docs(stem)

        # Build document stats
        self.build_doc_stats()

    def get_docs(self) -> List[dict]:
        """
        Parse the file into a list of documents.

        Returns:
            list: A list of dictionaries, where each dictionary represents a document.

        [
            {
                'doc_id': 2,
                'title': 'a new efficient structure-matching procedure and its application to automatic retrieval systems',
                'content': 'a new automatic method is presented for the comparison of two-dimensional line patterns .  retrieval applications include the matching of chemical structures, the comparison of syntactically analyzed excerpts extracted from documents and search requests, and the matching of document identifications consisting of twodimensional graphs with query identifications .',
            }
        ]
        """
        raise NotImplementedError

    def parse_docs(self, stem: bool = True):
        """
        Parse the documents into a list of dictionaries.

        - Tokenization
        - Removing stopwords

        Args:
            stem (bool): Whether to stem the tokens.
        """

        # Tokenization
        for doc in self.docs:
            doc["tokens"] = self.parser.parse(doc["content"], stem)
            self.word_set.update(doc["tokens"])

    def build_doc_stats(self):
        """
        Build stats for the documents.
        - Term frequency table
        - Word count table
        """

        word_list = list(self.word_set)
        word_list.sort()

        # Create a word count table
        self.tf_table = pd.DataFrame(
            0, index=[doc["doc_id"] for doc in self.docs], columns=word_list
        )

        for doc in self.docs:
            for token in doc["tokens"]:
                self.tf_table.at[doc["doc_id"], token] += 1
            for token in set(doc["tokens"]):
                self.wc_table[token] += 1

    def get_term_idfs(self) -> Dict[str, float]:
        """
        Extracts all term inverted document frequencies from stored
        documents.

        Returns:
            Inverted document frequencies for each term.
        """

        idfs = {}
        document_quantity = len(self.docs)

        for (term, df) in self.wc_table.items():
            idfs[term] = math.log(document_quantity / df)

        return idfs
