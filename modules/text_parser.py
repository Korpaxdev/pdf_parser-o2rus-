import re

from utils.constants import TemporaryFiles
from utils.file_utils import raise_exception_if_file_not_exists
from utils.patterns import Patterns


class TextParser:
    def __init__(self):
        raise_exception_if_file_not_exists(TemporaryFiles.PARSED_FILE)
        self._parsed_file = TemporaryFiles.PARSED_FILE
        self._parsed_data = []
        with self._parsed_file.open("r") as file:
            self._text = file.read()

    def parse(self):
        blocks = self._find_iterable_block(Patterns.BLOCK_ITEM, self._text)
        data_list = []
        for index, element in enumerate(blocks):
            data = dict()
            block_position_start = element.start()
            block_position_end = blocks[index + 1].start() if index + 1 < (len(blocks)) else None
            block_text = self._text[block_position_start:block_position_end]
            data_length = self._find_value(Patterns.BLOCK_DATA_LENGTH, block_text, "length")
            pgn = self._find_value(Patterns.BLOCK_DATA_PGN, block_text, "pgn")
            cat_id = self._find_value(Patterns.BLOCK_DATA_ID, block_text, "id")
            data["title"] = element.group(0)
            data["data_length"] = data_length
            data["pgn"] = pgn
            data["cat_id"] = cat_id
            data["params"] = self._find_params(block_text)
            data_list.append(data)

    def _find_params(self, block_text: str):
        params = self._find_value(Patterns.PARAMS_BLOCK_START, block_text)
        if not params:
            return []
        params_block_start = params.start()
        params_block_text = block_text[params_block_start:]
        params_data = []
        for param in self._find_iterable_block(Patterns.PARAMS, params_block_text):
            param_data = {"name": param.group("name"), "length": param.group("length"), "spn": param.group("spn")}
            param_data.update(self._find_detail_param_info(param.group("name"), param.group("paragraph")))
            params_data.append(param_data)
        return params_data

    def _find_detail_param_info(self, param_name: str, param_paragraph: str):
        param_detail_info = {"slot_scaling": None, "slot_range": None}
        param_info_pattern = Patterns.PARAM_BLOCK_PATTERN.format(
            name=re.escape(param_name), paragraph=re.escape(param_paragraph)
        )
        param_info_block = self._find_value(param_info_pattern, self._text)
        if not param_info_block:
            return param_detail_info
        param_info_block_start = param_info_block.start()
        param_info_block_text = self._text[param_info_block_start:]
        param_detail_info["slot_scaling"] = self._find_value(
            Patterns.PARAM_DETAIL_SLOT_SCALING_PATTERN, param_info_block_text, "slot_scaling"
        ).strip()
        param_detail_info["slot_range"] = self._find_value(
            Patterns.PARAM_DETAIL_SLOT_RANGE, param_info_block_text, "slot_range"
        )
        return param_detail_info

    @staticmethod
    def _find_iterable_block(pattern, text):
        return list(re.finditer(pattern, text, re.M))

    @staticmethod
    def _find_value(pattern: str, text: str, group_name: str = None):
        match = re.search(pattern, text, re.M)
        if not match:
            return None
        return match.group(group_name) if group_name else match
