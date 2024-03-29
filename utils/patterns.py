class Patterns:
    """
    Основные regexp паттерны
    BLOCK_PARAGRAPH - Параграф
    BLOCK_ITEM - Заголовок блока вместе с параграфом
    BLOCK_DATA_LENGTH - Параметр Data Length в блоке
    BLOCK_DATA_PARAMETER_GROUP - Параметр Parameter Group в блоке
    BLOCK_DATA_ID - Параметр ID в Parameter Group блока
    PARAMS_TABLE_HEAD - Таблица с параметрами блока
    PARAMS - Параметр в таблице PARAMS_TABLE_HEAD
    PARAM_BLOCK - Параграф и имя параметра (Для нахождения детальной информации по параметру)
    PARAM_DETAIL_LENGTH - Slot Length у параметра
    PARAM_DETAIL_SLOT_SCALING - Slot Scaling у параметра
    PARAM_DETAIL_SLOT_RANGE - Slot Range у параметра
    PARAM_DETAIL_SPN - SPN у параметра
    """

    BLOCK_PARAGRAPH = r"-71\s*5.3.\d+\?{0,2}"
    BLOCK_ITEM = BLOCK_PARAGRAPH + r"\s+([aA-zZ]+[/&#\s\w]+-\s+\w+)(?=\s)"
    BLOCK_DATA_LENGTH = r"Data\s*Length.*?(?P<length>\w+)"
    BLOCK_DATA_PARAMETER_GROUP = r"Parameter\s*Group"
    BLOCK_DATA_ID = BLOCK_DATA_PARAMETER_GROUP + r".*\(\s*(?P<id>\w+)\s*\)"
    PARAMS_TABLE_HEAD = r"POS Length\s*Parameter\s*Name\s*SPN and paragraph\s*Approved"
    PARAMS = r"(?:bits?|bytes?|Var\w+)\s*(?P<name>[A-Z]+.*?)\s{2,}\d{2,}\s*(?P<paragraph>[-\w]+\s*.*?)\s{2,}\d{1,}\/\d{1,}\/\d{4,}\s*"
    PARAM_BLOCK = r"\s*{paragraph}\s*{name}"
    PARAM_DETAIL_LENGTH = r"Slot\s*Length:\s*(?P<length>(?:\d+\s+\w+|[A-Z]+.*?))(?=\s{2,})"
    PARAM_DETAIL_SLOT_SCALING = r"Slot\s*Scaling:\s*(?P<slot_scaling>.*?)(?=,)"
    PARAM_DETAIL_SLOT_RANGE = r"Slot\s*Range:\s*(?P<slot_range>.*?)(?=Operational\s*Range)"
    PARAM_DETAIL_SPN = r"SPN:\s*(?P<spn>\d+)(?=\s)"
