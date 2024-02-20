from pathlib import Path


class TemporaryFiles:
    TEMP_DIR = Path("temp")
    PARSED_FILE = TEMP_DIR / "parsed.txt"


class ResultFiles:
    RESULT_DIR = Path("results")
    RESULT_FILE = RESULT_DIR / "result.json"
    RESULT_DB = RESULT_DIR / "result.db"


class ErrorMessages:
    BASE = "[bold red]Ошибка[/bold red]: %s"
    ARGUMENT_ERROR = BASE % "В качестве аргумента программы необходимо передать путь до pdf файла"
    FILE_NOT_FOUND = BASE % "Файл по пути: %s не был найден"
    FILE_EXTENSION = BASE % "Поддерживается только файл формата .pdf"
    ANSWER_ERROR = BASE % "Допустимые ответы - %s"


class SuccessMessages:
    BASE = "[bold green]Успешно[/bold green]: %s"
    SUCCESS_SAVE_TO_DB = BASE % "Данные успешно сохранены в db файл по пути %s"
    RESULT_FILE_CREATED = BASE % "Создан файл с результатами по пути %s"
    PDF_PARSING_SUCCESS = BASE % "Переведен файл %s в текстовый формат"


class WarningMessages:
    BASE = "[bold yellow]ВНИМАНИЕ[/bold yellow]: %s"
    CHECK_RESULT_FILE_BEFORE_SAVE = BASE % (
        "Проверьте результирующий файл по пути %s.\n"
        "В случае если в данных есть ошибка, отредактируйте файл (или паттерны regexp и вновь запустите парсинг).\n"
        f"После проверки файла вы можете сохранить результирующие данные из файла {ResultFiles.RESULT_FILE.name} в базу данных\n"
    )


class Messages:
    HELLO_MESSAGE = "Программа для парсинга pdf файлов и сохранения результата в бд"
    FILE_HELP = "PDF Файл для парсинга"
    PDF_PARSING_START = "Произвожу парсинг файла %s"
    TEXT_PARSING_START = "Произвожу парсинг блоков"
    SAVE_TO_DB_PROMPT = "Желаете сохранить данные в базу данных?(Y/n): "
    SAVING_DATA_TO_DB = "Произвожу сохранение данных в базу данных"
    ONLY_SAVE_DB = (
        f"Позволяет сохранить данные из {ResultFiles.RESULT_FILE.name} в базу данных."
        f"Использование возможно только в случае уже сгенерированного файла {ResultFiles.RESULT_FILE.name}"
    )


class SaveToDB:
    YES = "Y"
    NO = "N"
    LIST_VALUES = [YES, NO]
