# coding=utf-8
"""
elib_miz exceptions
"""


class ELIBMizError(Exception):
    """
    Base elib_miz error
    """
    pass


class MizFileNotFoundError(ELIBMizError):
    """
    Raised when a given MIZ file wasn't found
    """

    def __init__(self, miz_file_path: str) -> None:
        self.miz_file_path = miz_file_path
        super(MizFileNotFoundError, self).__init__(f'MIZ file not found: {miz_file_path}')


class MizFileAlreadyExistsError(ELIBMizError):
    """
    Raised when a given MIZ file already exists and would be overwritten
    """

    def __init__(self, miz_file_path: str) -> None:
        self.miz_file_path = miz_file_path
        super(MizFileAlreadyExistsError, self).__init__(f'MIZ file already exists: {miz_file_path}')


class InvalidDateTimeString(ELIBMizError):
    """
    Raised when a given MIZ file already exists and would be overwritten
    """

    def __init__(self, time_str: str) -> None:
        self.time_str = time_str
        super(InvalidDateTimeString, self).__init__(f'invalid time string: {time_str}')
