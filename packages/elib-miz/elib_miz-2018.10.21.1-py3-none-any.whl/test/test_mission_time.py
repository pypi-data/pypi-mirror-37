# coding=utf-8
import datetime
from pathlib import Path

import pytest
from hypothesis import given, settings, strategies as st

from elib_miz import MissionTime, exc
from elib_miz.miz import Miz

_DUMMY_DT = datetime.datetime.now()


@given(example_datetime=st.datetimes(
    min_value=_DUMMY_DT.replace(year=1900),
    max_value=_DUMMY_DT.replace(year=2050),
))
@settings(max_examples=500)
def test_from_string(example_datetime: datetime.datetime):
    example_datetime = example_datetime.replace(tzinfo=None, microsecond=0)
    year = example_datetime.year
    month = example_datetime.month
    day = example_datetime.day
    hour = example_datetime.hour
    minute = example_datetime.minute
    second = example_datetime.second
    input_string = f'{year:04d}{month:02d}{day:02d}{hour:02d}{minute:02d}{second:02d}'
    time = MissionTime.from_string(input_string)
    assert isinstance(time, MissionTime)
    assert time.year == year
    assert time.month == month
    assert time.day == day
    assert time.hour == hour
    assert time.minute == minute
    assert time.second == second
    assert isinstance(time.mission_start_time, int)
    assert example_datetime == time.datetime


def test_now():
    now = datetime.datetime.utcnow()
    now = now.replace(tzinfo=None, microsecond=0)
    time = MissionTime.now()
    assert time.datetime - now <= datetime.timedelta(seconds=1)


@pytest.mark.long
@pytest.mark.cover
@given(example_datetime=st.datetimes(
    min_value=_DUMMY_DT.replace(year=1900),
    max_value=_DUMMY_DT.replace(year=2050),
))
@settings(max_examples=10, deadline=9999)
def test_apply_to_miz(test_file, example_datetime):
    result_miz = './test.miz'
    example_datetime = example_datetime.replace(tzinfo=None, microsecond=0)
    if example_datetime.day == 31:
        example_datetime = example_datetime.replace(day=30)
    year = example_datetime.year
    month = example_datetime.month
    day = example_datetime.day
    hour = example_datetime.hour
    minute = example_datetime.minute
    second = example_datetime.second
    input_string = f'{year:04d}{month:02d}{day:02d}{hour:02d}{minute:02d}{second:02d}'
    time = MissionTime.from_string(input_string)
    time.apply_to_miz(test_file, result_miz, overwrite=True)
    with Miz(result_miz) as miz:
        # original_start_time = miz.mission.mission_start_time
        # assert miz.mission.mission_start_time != original_start_time
        assert time.day == miz.mission.day
        assert time.month == miz.mission.month
        assert time.year == miz.mission.year
        assert time.mission_start_time == miz.mission.mission_start_time


def test_from_miz(latest_test_file):
    mission_time = MissionTime.from_miz(str(latest_test_file))
    assert 'MissionTime(year=2011, month=6, day=1, hour=12, minute=0, second=0)' == mission_time.__repr__()
    assert '2011-06-01T12:00:00' == mission_time.iso_format


def test_from_miz_missing_file():
    with pytest.raises(exc.MizFileNotFoundError):
        MissionTime.from_miz('./test.miz')


@pytest.mark.parametrize(
    'invalid_string',
    [
        'somerandomstring',
        '0000000000000',
        '000000000000000',
    ]
)
def test_from_string_invalid_string(invalid_string):
    with pytest.raises(exc.InvalidDateTimeString):
        MissionTime.from_string(invalid_string)


def test_date_time_prop():
    mission_time = MissionTime.now()
    assert mission_time.datetime is mission_time.datetime


def test_apply_to_miz_file_errors():
    in_file = Path('in.miz')
    out_file = Path('out.miz')
    out_file.touch()
    mission_time = MissionTime.now()
    with pytest.raises(exc.MizFileNotFoundError):
        mission_time.apply_to_miz(str(in_file), str(out_file))
    in_file.touch()
    with pytest.raises(exc.MizFileAlreadyExistsError):
        mission_time.apply_to_miz(str(in_file), str(out_file))
