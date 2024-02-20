from pathlib import Path
from shutil import rmtree

from utils.exceptions import FileNotFoundException


def create_dir(path: Path):
    """Утилита для создания директории"""
    path.mkdir(parents=True, exist_ok=True)
    return path


def raise_exception_if_file_not_exists(path: Path):
    """Утилита для создания исключения FileNotFoundException если файл не существует или не является файлом"""
    if not path.exists() or not path.is_file():
        raise FileNotFoundException(FileNotFoundException.message % path.absolute())


def remove_dir_if_exists(path: Path):
    """Утилита для удаления всей директории вместе с файлами"""
    if path.exists():
        rmtree(path)
