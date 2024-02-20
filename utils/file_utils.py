from os import remove
from pathlib import Path
from shutil import rmtree

from utils.exceptions import FileNotFoundException


def create_dir(path: Path):
    path.mkdir(parents=True, exist_ok=True)
    return path


def remove_file_if_exists(path: Path):
    if path.exists():
        remove(path)
    return path


def raise_exception_if_file_not_exists(path: Path):
    if not path.exists() or not path.is_file():
        raise FileNotFoundException(FileNotFoundException.message % path.absolute())


def remove_dir_if_exists(path: Path):
    if path.exists():
        rmtree(path)
