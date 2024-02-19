import argparse
import json
from pathlib import Path

from rich.console import Console

from modules.database.models import Block
from modules.database.service import DBService
from modules.pdf_parser import PdfParser
from modules.text_parser import TextParser
from utils.constants import (
    TemporaryFiles,
    Messages,
    ErrorMessages,
    SaveToDB,
    ResultFiles,
    WarningMessages,
    SuccessMessages,
)
from utils.exceptions import FileNotFoundException, FileExtensionException
from utils.file_utils import remove_dir_if_exists


class App:
    def __init__(self):
        self._clear_temp_directory()
        self._console = Console()
        self._file_path = self._get_file_path()
        self._pdf_parser = PdfParser(self._file_path, self._console)
        self._text_parser = TextParser(self._console)
        self._db_service = DBService()

    def run(self):
        self._pdf_parser.parse()
        self._text_parser.parse()
        self._console.print(WarningMessages.CHECK_RESULT_FILE_BEFORE_SAVE % ResultFiles.RESULT_FILE.absolute())
        allow_save_to_db = self._get_user_answer(Messages.SAVE_TO_DB_PROMPT, SaveToDB.LIST_VALUES, SaveToDB.YES)

        if allow_save_to_db == SaveToDB.YES:
            with self._console.status(Messages.SAVING_DATA_TO_DB) as status:
                self._db_service.clear_database()
                self._db_service.insert_all(self._create_block_models_from_file(ResultFiles.RESULT_FILE))
                status.console.log(SuccessMessages.SUCCESS_SAVE_TO_DB % self._db_service.db_path.absolute())

        self._clear_temp_directory()

    def _get_file_path(self):
        arg_parser = argparse.ArgumentParser(description=Messages.HELLO_MESSAGE)
        arg_parser.add_argument("filename", help=Messages.FILE_HELP)
        args = arg_parser.parse_args()
        file_path = Path(args.filename)
        try:
            if not file_path.is_file() or not file_path.exists():
                raise FileNotFoundException(FileNotFoundException.message % file_path.absolute())
            if file_path.suffix != ".pdf":
                raise FileExtensionException
            return file_path
        except (FileNotFoundException, FileExtensionException) as e:
            self._console.print(ErrorMessages.BASE, e.message)

    @staticmethod
    def _clear_temp_directory():
        remove_dir_if_exists(TemporaryFiles.TEMP_DIR)

    def _get_user_answer(self, prompt: str, valid_names: list[str], default: str = ""):
        valid_names = [name.upper() for name in valid_names]
        user_answer = self._console.input(prompt).strip().upper()
        while user_answer not in valid_names:
            if not user_answer and default:
                return default
            self._console.print(ErrorMessages.ANSWER_ERROR % " | ".join(valid_names))
            user_answer = self._console.input(prompt).strip().upper()
        return user_answer

    @staticmethod
    def _create_block_models_from_file(result_file: Path):
        block_param_list = []
        with result_file.open() as f:
            for block in json.load(f):
                for block_params in block["params"]:
                    block_model = Block(
                        cat_id=block["cat_id"],
                        data_length=block["data_length"],
                        name=block_params["name"],
                        length=block_params["length"],
                        scaling=block_params["scaling"],
                        range=block_params["range"],
                        spn=block_params["spn"],
                    )
                    block_param_list.append(block_model)
        return block_param_list
