from os import remove
from pathlib import Path


def create_dir(path: Path):
    path.mkdir(parents=True, exist_ok=True)
    return path


def remove_file_if_exists(path: Path):
    if path.exists():
        remove(path)
    return path
