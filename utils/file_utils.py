from os import remove
from pathlib import Path


def create_dir(path: Path):
    path.mkdir(parents=True, exist_ok=True)
    return path


def remove_file_if_exists(path: Path):
    if path.exists():
        remove(path)
    return path


def raise_exception_if_file_not_exists(path: Path):
    if not path.is_file() and not path.exists():
        raise FileExistsError(f"Файл по пути {path.absolute()} не найден")
