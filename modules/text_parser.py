import json
import re

from rich.console import Console
from rich.progress import track

from utils.constants import TemporaryFiles, Messages, ResultFiles, SuccessMessages
from utils.file_utils import raise_exception_if_file_not_exists, create_dir
from utils.patterns import Patterns


class TextParser:
    def __init__(self, console: Console):
        self._console = console
        self._parsed_file = TemporaryFiles.PARSED_FILE
        create_dir(ResultFiles.RESULT_DIR)
        self._result_file = ResultFiles.RESULT_FILE
        self._parsed_data = []
        self._text = ""

    def parse(self):
        raise_exception_if_file_not_exists(TemporaryFiles.PARSED_FILE)
        self._read_parsed_file()

        blocks = self._find_iterable_block(Patterns.BLOCK_ITEM, self._text)
        data_list = []

        for index, element in track(
            enumerate(blocks), total=len(blocks), description=Messages.TEXT_PARSING_START, console=self._console
        ):
            data = dict()
            block_position_start = element.start()
            block_position_end = blocks[index + 1].start() if index + 1 < (len(blocks)) else None
            block_text = self._text[block_position_start:block_position_end]
            data_length = self._find_value(Patterns.BLOCK_DATA_LENGTH, block_text)
            cat_id = self._find_value(Patterns.BLOCK_DATA_ID, block_text)
            data["title"] = element.group(1)
            data["data_length"] = data_length
            data["cat_id"] = cat_id
            data["params"] = self._find_params(block_text)
            data_list.append(data)

        with self._result_file.open("w") as file:
            json.dump(data_list, file, indent=4)
        self._console.log(SuccessMessages.RESULT_FILE_CREATED % self._result_file.absolute())

    def _find_params(self, block_text: str):
        params_table_head = self._find_value(Patterns.PARAMS_TABLE_HEAD, block_text)

        if not params_table_head:
            return []

        params_table_start = params_table_head.start()
        params_table_text = block_text[params_table_start:]
        params_data = []

        for param in self._find_iterable_block(Patterns.PARAMS, params_table_text):
            params_info = self._find_detail_param_info(param.group("name"), param.group("paragraph"))

            if not params_info:
                continue

            param_data = {"name": param.group("name"), **params_info}
            params_data.append(param_data)

        return params_data

    def _find_detail_param_info(self, param_name: str, param_paragraph: str):
        param_info_pattern = Patterns.PARAM_BLOCK.format(
            name=re.escape(param_name), paragraph=re.escape(param_paragraph)
        )
        param_info_block = self._find_value(param_info_pattern, self._text)

        if not param_info_block:
            return

        param_detail_info = dict()
        param_info_block_start = param_info_block.start()
        param_info_block_text = self._text[param_info_block_start:]
        param_detail_info["length"] = self._find_value(Patterns.PARAM_DETAIL_LENGTH, param_info_block_text)
        param_detail_info["rus_name"] = None
        param_detail_info["scaling"] = self._find_value(Patterns.PARAM_DETAIL_SLOT_SCALING, param_info_block_text)
        param_detail_info["range"] = self._find_value(Patterns.PARAM_DETAIL_SLOT_RANGE, param_info_block_text)
        param_detail_info["spn"] = self._find_value(Patterns.PARAM_DETAIL_SPN, param_info_block_text)

        return param_detail_info

    @staticmethod
    def _find_iterable_block(pattern, text):
        return list(re.finditer(pattern, text, re.M))

    @staticmethod
    def _find_value(pattern: str, text: str, group_name: str = ""):
        match = re.search(pattern, text, re.M)

        if not match:
            return None
        if group_name:
            return match.group(group_name).strip()

        return match.group(1).strip() if match.groups() else match

    def _read_parsed_file(self):
        with open(self._parsed_file) as file:
            self._text = file.read()
