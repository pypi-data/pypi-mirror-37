# coding=utf-8

import calendar

import pytest
from hypothesis import given, strategies as st

from elib_miz.mission import Mission


def test_mission_year_get(mission: Mission):
    assert mission.year == 2011


@given(year=st.integers(min_value=1900, max_value=2100))
def test_mission_year_set(mission: Mission, year):
    mission.year = year
    assert mission.year == year


def test_mission_month_get(mission):
    assert mission.month == 6


@given(month=st.integers(min_value=1, max_value=12))
def test_mission_month_set(mission, month):
    mission.month = month
    assert mission.month == month


@given(day=st.integers(min_value=1, max_value=30))
def test_mission_day(mission, day):
    mission.day = day
    assert mission.day == day


@pytest.mark.parametrize(
    'month,day',
    [
        (1, 31),
        (2, 28),
        (3, 31),
        (4, 30),
        (5, 31),
        (6, 30),
        (7, 31),
        (8, 31),
        (9, 30),
        (10, 31),
        (11, 30),
        (12, 31),
    ]
)
def test_mission_day_limit(mission, month, day):
    mission.month = month
    mission.day = 31
    assert mission.day == day


@given(hour=st.integers(min_value=0, max_value=23))
def test_mission_hour(mission, hour):
    mission.hour = hour
    assert mission.hour == hour


@given(minute=st.integers(min_value=0, max_value=59))
def test_mission_minute(mission, minute):
    mission.minute = minute
    assert mission.minute == minute


@given(second=st.integers(min_value=0, max_value=59))
def test_mission_second(mission, second):
    mission.second = second
    assert mission.second == second


@given(
    year=st.integers(min_value=1900, max_value=2100),
    month=st.integers(min_value=1, max_value=12),
    day=st.integers(min_value=1, max_value=30),
    hour=st.integers(min_value=0, max_value=23),
    minute=st.integers(min_value=0, max_value=59),
    second=st.integers(min_value=0, max_value=59)
)
def test_mission_datetime_mixed_in(mission, year, month, day, hour, minute, second):
    mission.year = year
    mission.month = month
    mission.day = day
    mission.hour, mission.minute, mission.second = hour, minute, second
    assert mission.year == year
    assert mission.month == month
    if day > calendar.monthrange(year, month)[1]:
        expected_day = calendar.monthrange(year, month)[1]
    else:
        expected_day = day
    assert mission.day == expected_day
    assert mission.minute == minute
    assert mission.second == second
