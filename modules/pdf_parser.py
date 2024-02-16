from pathlib import Path

from PyPDF2 import PdfReader

from utils.constants import TemporaryFiles
from utils.file_utils import create_dir, remove_file_if_exists


class PdfParser:
    def __init__(self, file_path: Path | str):
        if not isinstance(file_path, Path):
            file_path = Path(file_path)
        if not file_path.is_file() and not file_path.exists():
            raise FileExistsError("Файл не существует")
        self._file_path = file_path
        self._parser = PdfReader(self._file_path)
        self._temp_dir = create_dir(TemporaryFiles.TEMP_DIR)
        self._parsed_file = remove_file_if_exists(TemporaryFiles.PARSED_FILE)

    def parse(self) -> Path:
        with self._parsed_file.open("w") as file:
            for page in self._parser.pages:
                file.write(page.extract_text())
        return self._parsed_file
