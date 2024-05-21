import nltk
from typing import List
import string

class BaseParser:
    """
    Class to tokenize and parse the documents or queries.
    """

    def __init__(self, lang="english"):
        self.stopwords = set(nltk.corpus.stopwords.words(lang) + list(string.ascii_lowercase))
        self.stemmer = nltk.PorterStemmer()

    def parse(self, text: str, stem: bool = False) -> List[str]:
        # Tokenize the the content
        text = nltk.word_tokenize(text)

        # Lowercase the tokens to normalize
        text = [token.lower() for token in text]

        # Remove non-alphanumeric characters and not only numbers
        text = [
            token for token in text if token.isalnum() and not token.isdigit() or "'" in token
        ]

        # Remove apostrophes in the middle of a token
        text = [token.replace("'", "") for token in text]

        # Remove apostrophes at the beginning or end of a token
        text = [token.strip("'") for token in text]

        # Remove stopwords
        text = [
            token for token in text if token not in self.stopwords
        ]

        # Stemming
        if stem:
            text = [self.stemmer.stem(token) for token in text]

        return text