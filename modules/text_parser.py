import json
import re

from rich.console import Console
from rich.progress import track

from utils.constants import TemporaryFiles, Messages, ResultFiles, SuccessMessages
from utils.file_utils import raise_exception_if_file_not_exists, create_dir
from utils.patterns import Patterns


class TextParser:
    """Класс для парсинга txt файла с помощью regexp в json объект"""

    def __init__(self, console: Console):
        self._console = console
        self._parsed_file = TemporaryFiles.PARSED_FILE
        create_dir(ResultFiles.RESULT_DIR)
        self._result_file = ResultFiles.RESULT_FILE
        self._parsed_data = []
        self._text = ""

    def parse(self):
        """
        Производит парсинг PARSED_FILE по этапам:
        1. Находит расположение blocks по BLOCK_ITEM pattern
        2. Вытаскивает информацию по каждому block in blocks (title, data_length, id)
        3. Находит список детальной информации по параметрам блока (params)
        4. Создает список с информацией по блоку
        5. Записывает этот список в self._result_file
        """
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
            data["id"] = cat_id
            data["params"] = self._find_params(block_text)
            data_list.append(data)

        with self._result_file.open("w") as file:
            json.dump(data_list, file, indent=4)
        self._console.log(SuccessMessages.RESULT_FILE_CREATED)

    def _find_params(self, block_text: str):
        """
        Находит параметры в block_text.
        Находит детальную информацию по параметрам.
        Возвращает список с детальной информацией по параметрам блока.
        :param block_text:str - Текст с информацией по блоку
        :return: params_data: list[dict] - список с детальной информацией по параметрам блока
        """
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
        """
        Находит в self_text расположение детальной информации по r\s*{param_paragraph}\s*{param_name} паттерну
        Достает из этого расположения информацию: length, scaling, range, spn
        :param param_name: str Имя параметра
        :param param_paragraph: str Параграф параметра
        :return: param_detail_info: dict - словарь с детальной информацией по параметру
        """
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
        """
        Возвращает список всех найденных значений из строки text по pattern
        :param pattern: str с regexp паттерном
        :param text: str текст, на котором необходимо применить pattern
        :return: list[Match] - список совпадений с pattern
        """
        return list(re.finditer(pattern, text, re.M))

    @staticmethod
    def _find_value(pattern: str, text: str, group_name: str = ""):
        """
        Ищет совпадения по pattern в строке text.
        Если совпадений нет возвращает None.
        Если есть совпадения, то возвращает их.
        :param pattern: str с regexp паттерном
        :param text: str текст, на котором необходимо применить pattern
        :param group_name: default = "", имя группы, которое необходимо вернуть
        :return: None | str | Match[str] - совпадение с pattern
        """
        match = re.search(pattern, text, re.M)

        if not match:
            return None
        if group_name:
            return match.group(group_name).strip()

        return match.group(1).strip() if match.groups() else match

    def _read_parsed_file(self):
        """
        Считывает информацию из txt файла в переменную self._text
        """
        with open(self._parsed_file) as file:
            self._text = file.read()
