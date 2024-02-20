from pathlib import Path

from PyPDF2 import PdfReader
from rich.console import Console

from utils.constants import TemporaryFiles, Messages, SuccessMessages
from utils.file_utils import create_dir


class PdfParser:
    """Класс для парсинга pdf файла в txt"""

    def __init__(self, file_path: Path | str, console: Console):
        if not isinstance(file_path, Path):
            file_path = Path(file_path)
        self._console = console
        self._file_path = file_path
        self._parser = PdfReader(self._file_path)
        create_dir(TemporaryFiles.TEMP_DIR)
        self._parsed_file = TemporaryFiles.PARSED_FILE

    def parse(self):
        """
        Производит парсинг pdf файла и сохраняет результат в PARSED_FILE
        :return: self._parsed_file: Path
        """
        with self._console.status(Messages.PDF_PARSING_START % self._file_path.name) as status:
            with self._parsed_file.open("w") as file:
                for page in self._parser.pages:
                    file.write(page.extract_text())
            status.console.log(SuccessMessages.PDF_PARSING_SUCCESS % self._file_path.name)
        return self._parsed_file
