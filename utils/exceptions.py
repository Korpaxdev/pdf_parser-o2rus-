from utils.constants import ErrorMessages


class CustomException(Exception):
    message: str = ""

    def __init__(self, custom_message: str = ""):
        if custom_message:
            self.message = custom_message

    def __str__(self):
        return self.message


class FileNotFoundException(CustomException):
    message = ErrorMessages.FILE_NOT_FOUND


class FileExtensionException(CustomException):
    message = ErrorMessages.FILE_EXTENSION
