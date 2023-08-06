# coding=utf-8

import os
from pathlib import Path

import pytest

from elib_miz import Mission, Miz


@pytest.mark.parametrize('cls', [Miz])
def test_init(tmpdir, cls):
    t = Path(str(tmpdir))

    f = t.joinpath('f.txt')

    with pytest.raises(FileNotFoundError):
        cls(f)

    with pytest.raises(TypeError):
        cls(t)

    f.write_text('')

    with pytest.raises(ValueError):
        cls(f)

    f = t.joinpath('f.miz')
    f.write_text('')

    cls(f)


def test_unzip(test_file):
    m = Miz(test_file)
    m.unzip()


def test_mission_dict(test_file):
    m = Miz(test_file)
    with pytest.raises(RuntimeError):
        assert m.mission
    m.unzip()
    m.decode()
    assert isinstance(m.mission, Mission)


def test_l10n_dict(test_file):
    m = Miz(test_file)
    with pytest.raises(RuntimeError):
        assert m.l10n
    m.unzip()
    m.decode()
    assert isinstance(m.l10n, dict)


def test_map_resources(test_file):
    m = Miz(test_file)
    with pytest.raises(RuntimeError):
        assert m.map_res
    m.unzip()
    m.decode()
    assert isinstance(m.map_res, dict)


def test_resources(test_file):
    m = Miz(test_file)
    assert isinstance(m.resources, set)
    assert not m.resources


def test_context(test_file):
    with Miz(test_file) as miz:
        assert isinstance(miz.mission, Mission)
        tmpdir = os.path.abspath(miz.temp_dir)

    assert not os.path.exists(tmpdir)


def test_fog(dust_miz_file):
    with Miz(dust_miz_file) as miz:
        assert miz.mission.weather.dust_enabled is True
        assert miz.mission.weather.dust_density == 2233
        assert miz.mission.theatre == 'PersianGulf'
