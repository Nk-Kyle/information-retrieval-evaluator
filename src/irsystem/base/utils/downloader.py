from pathlib import Path
from typing import List, Any
from nltk.downloader import Downloader
import nltk
import logging

def check_package_exists(
    package_id: Any,
    download_dir: Path,
) -> bool:
    downloader = Downloader(download_dir=str(download_dir))
    return downloader.is_installed(package_id)

def download_nltk_data(
    list_of_resources: List[str],
    download_dir: Path,
) -> None:
    download_dir.mkdir(parents=True, exist_ok=True)
    downloader = Downloader(download_dir=str(download_dir))
    for resource in list_of_resources:
        if not check_package_exists(resource, download_dir):
            logging.debug(f'Downloading {resource} to {download_dir}')
            downloader.download(info_or_id=resource, quiet=True)
        else:
            logging.debug(f'{resource} already exists in {download_dir}')

    nltk.data.path.append(str(download_dir))