# coding=utf-8
"""
Manages date and time in a mission
"""
import datetime as base_datetime
import re
from pathlib import Path

import dataclasses

from elib_miz import LOGGER, Miz
from elib_miz.exc import InvalidDateTimeString, MizFileAlreadyExistsError, MizFileNotFoundError

RE_INPUT_STRING = re.compile(r'^'
                             r'(?P<year>[\d]{4})'
                             r'(?P<month>[\d]{2})'
                             r'(?P<day>[\d]{2})'
                             r'(?P<hour>[\d]{2})'
                             r'(?P<minute>[\d]{2})'
                             r'(?P<second>[\d]{2})'
                             r'$')


@dataclasses.dataclass
class MissionTime:
    """
    Represents a date-time object with convenience methods for MIZ files
    """
    year: int
    month: int
    day: int
    hour: int
    minute: int
    second: int

    @staticmethod
    def from_datetime(datetime_: base_datetime.datetime) -> 'MissionTime':
        """
        Creates MissionTime from datetime.Datetime object

        :param datetime_: source datetime.datetime
        :type datetime_: datetime.datetime
        :return: MissionTime object
        :rtype: MissionTime
        """
        return MissionTime(
            datetime_.year,
            datetime_.month,
            datetime_.day,
            datetime_.hour,
            datetime_.minute,
            datetime_.second
        )

    @staticmethod
    def now() -> 'MissionTime':
        """
        Creates a MissionTime object from the current UTC time

        :return: MissionTime object
        :rtype: MissionTime
        """
        return MissionTime.from_datetime(base_datetime.datetime.utcnow())

    @staticmethod
    def from_miz(miz_file_path: str) -> 'MissionTime':
        """
        Creates a MissionTime object from a MIZ file

        :param miz_file_path: path to the source MIZ file
        :type miz_file_path: str
        :return: MissionTime object
        :rtype: MissionTime
        """
        _miz_file_path = Path(miz_file_path).absolute()
        if not _miz_file_path.exists():
            raise MizFileNotFoundError(str(_miz_file_path))
        with Miz(str(_miz_file_path)) as miz:
            _year = miz.mission.year
            _month = miz.mission.month
            _day = miz.mission.day
            _minute, _second = divmod(miz.mission.mission_start_time, 60)
            _hour, _minute = divmod(_minute, 60)
        return MissionTime(_year, _month, _day, _hour, _minute, _second)

    @staticmethod
    def from_string(datetime_str: str) -> 'MissionTime':
        """
        Create a MissionTime object from a given string

        String format must be:

            YYYYMMDDhhmmss

        :param datetime_str: source string
        :type datetime_str: str
        :return: MissionTime object
        :rtype: MissionTime
        """

        match = RE_INPUT_STRING.match(datetime_str)
        if not match:
            raise InvalidDateTimeString(datetime_str)

        return MissionTime(
            int(match.group('year')),
            int(match.group('month')),
            int(match.group('day')),
            int(match.group('hour')),
            int(match.group('minute')),
            int(match.group('second')),
        )

    @property
    def datetime(self) -> base_datetime.datetime:
        """
        :return: datetime object representing this MissionTime
        :rtype: datetime.datetime
        """
        if not hasattr(self, '__datetime'):
            dt_obj = base_datetime.datetime(self.year, self.month, self.day, self.hour, self.minute, self.second)
            setattr(self, '__datetime', dt_obj)
        return getattr(self, '__datetime')

    @property
    def mission_start_time(self) -> int:
        """
        :return: mission start time as per DCS standards
        :rtype: int
        """
        return self.hour * 3600 + self.minute * 60 + self.second

    @property
    def iso_format(self) -> str:
        """
        :return: this MissionTime in ISO8601 format
        :rtype: str
        """
        return self.datetime.isoformat()

    def apply_to_miz(self, source_miz_file: str, out_miz_file: str, overwrite: bool = False) -> None:
        """
        Applies this MissionTime to a MIZ file

        :param source_miz_file: path to the source MIZ file
        :type source_miz_file: str
        :param out_miz_file: path to the target MIZ file
        :type out_miz_file: str
        :param overwrite: whether or not to overwrite an existing target file
        :type overwrite: bool
        """
        _source_miz_file_path = Path(source_miz_file).absolute()
        _out_miz_file_path = Path(out_miz_file).absolute()
        if not _source_miz_file_path.exists():
            raise MizFileNotFoundError(str(_source_miz_file_path))
        if _out_miz_file_path.exists() and not overwrite:
            raise MizFileAlreadyExistsError(str(_out_miz_file_path))
        with Miz(str(_source_miz_file_path)) as miz:
            LOGGER.debug('applying time to miz: %s', self.iso_format)
            miz.mission.day = self.day
            miz.mission.month = self.month
            miz.mission.year = self.year
            miz.mission.mission_start_time = self.mission_start_time
            miz.zip(str(_out_miz_file_path))
