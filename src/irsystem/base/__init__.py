from .reader import BaseDocReader
from .query import BaseQueryReader
from .utils.downloader import download_nltk_data
from pathlib import Path

download_nltk_data(
    list_of_resources=[
        'stopwords',
        "punkt",
    ],
    download_dir=Path('./data/nltk/'),
)