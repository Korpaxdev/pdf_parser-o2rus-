from pathlib import Path


class TemporaryFiles:
    """
    Содержит константы для временных файлов:
    TEMP_DIR - временная директория
    PARSED_FILE - txt файл с результатом парсинга
    """

    TEMP_DIR = Path("temp")
    PARSED_FILE = TEMP_DIR / "parsed.txt"


class ResultFiles:
    """
    Содержит константы для результирующих файлов:
    RESULT_DIR - директория с результирующими файлами
    RESULT_FILE - json файл с результатом работы txt прасинга
    RESULT_DB - база данных, при сохранении RESULT_FILE в бд
    """

    RESULT_DIR = Path("results")
    RESULT_FILE = RESULT_DIR / "result.json"
    RESULT_DB = RESULT_DIR / "result.db"


class SaveToDBAnswers:
    """
    Содержит константы разрешенных ответов пользователя на сохранения информации в бд
    """

    YES = "Y"
    NO = "N"
    LIST_VALUES = [YES, NO]

    @classmethod
    def get_string_values(cls):
        return ", ".join(cls.LIST_VALUES)


class ErrorMessages:
    """
    Константы для сообщений об ошибках
    """

    BASE = "[bold red]Ошибка[/bold red]: %s"
    ARGUMENT_ERROR = BASE % "В качестве аргумента программы необходимо передать путь до pdf файла"
    FILE_NOT_FOUND = BASE % "Файл по пути: %s не был найден"
    FILE_EXTENSION = BASE % "Поддерживается только файл формата .pdf"
    SAVE_TO_DB_ANSWER = BASE % f"Допустимые ответы - {SaveToDBAnswers.get_string_values()}"


class SuccessMessages:
    """
    Константы для успешных сообщений
    """

    BASE = "[bold green]Успешно[/bold green]: %s"
    SUCCESS_SAVE_TO_DB = BASE % f"Данные успешно сохранены в db файл по пути {ResultFiles.RESULT_DB.absolute()}"
    RESULT_FILE_CREATED = BASE % f"Создан файл с результатами по пути {ResultFiles.RESULT_FILE.absolute()}"
    PDF_PARSING_SUCCESS = BASE % "Переведен файл %s в текстовый формат"


class WarningMessages:
    """
    Константы для предупреждающих сообщений
    """

    BASE = "[bold yellow]ВНИМАНИЕ[/bold yellow]: %s"
    CHECK_RESULT_FILE_BEFORE_SAVE = BASE % (
        f"Проверьте результирующий файл перед сохранением в базу данных по пути {ResultFiles.RESULT_FILE.absolute()}\n"
        "Если в файле есть ошибки отредактируйте их и только тогда сохраняйте в базу данных.\n"
        "Так же вы можете отредактировать паттерны regexp и запустить парсинг повторно.\n"
        f"Обратите внимание, что процесс сохранения данных из {ResultFiles.RESULT_FILE} в бд можно запустить вручную позже с помощью флага --only_save_db"
    )


class Messages:
    """
    Константы для информирующих сообщений
    """

    HELLO_MESSAGE = "Программа для парсинга pdf файлов и сохранения результата в бд"
    FILE_HELP = "PDF Файл для парсинга"
    PDF_PARSING_START = "Произвожу парсинг файла %s"
    TEXT_PARSING_START = "Произвожу парсинг блоков"
    SAVE_TO_DB_PROMPT = "Желаете сохранить данные в базу данных?(y/N): "
    SAVING_DATA_TO_DB = "Произвожу сохранение данных в базу данных"
    ONLY_SAVE_DB = (
        f"Позволяет сохранить данные из {ResultFiles.RESULT_FILE.name} в базу данных."
        f"Использование возможно только в случае уже сгенерированного файла {ResultFiles.RESULT_FILE.name}"
    )
