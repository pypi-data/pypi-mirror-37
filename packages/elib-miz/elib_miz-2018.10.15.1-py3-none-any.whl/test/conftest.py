# coding=utf-8
import copy
import os
import sys
from pathlib import Path

import pytest
# import logging
from mockito import unstub

from elib_miz import Mission, Miz


# noinspection PyUnusedLocal
def pytest_configure(config):
    sys._called_from_test = True


# noinspection PyUnusedLocal,SpellCheckingInspection
def pytest_unconfigure(config):
    # noinspection PyUnresolvedReferences,PyProtectedMember
    del sys._called_from_test


# @pytest.fixture(scope='session', autouse=True)
# def _setup_logging():
#     logger = elib.custom_logging.get_logger('EMIZ')
#     elib.custom_logging.set_root_logger(logger)
#     for handler in logger.handlers:
#         handler.setLevel(10)


@pytest.fixture(autouse=True)
def _all(request, tmpdir, out_file: Path):
    if out_file.exists():
        out_file.unlink()
    if 'nocleandir' in request.keywords:
        yield
    else:
        current_dir = os.getcwd()
        os.chdir(str(tmpdir))
        yield os.getcwd()
        os.chdir(current_dir)
    unstub()
    if out_file.exists():
        out_file.unlink()


def pytest_addoption(parser):
    parser.addoption("--long", action="store_true",
                     help="run long tests")


def pytest_runtest_setup(item):
    longmarker = item.get_marker("long")
    if longmarker is not None and not item.config.getoption('long'):
        pytest.skip('skipping long tests')


TEST_FILES_FOLDER = Path('./test/test_files').absolute()
if not TEST_FILES_FOLDER.exists():
    raise RuntimeError('cannot find test files')

SLTP_TEST_FILE = Path(TEST_FILES_FOLDER, 'sltp').absolute()
if not SLTP_TEST_FILE.exists():
    raise RuntimeError('cannot find SLTP test files')


# @pytest.fixture(name='test_files_folder')
# def _test_files_folder():
#     yield TEST_FILES_FOLDER


@pytest.fixture(
    params=('TRG_KA50.miz', 'test_158.miz', 'test_252.miz', 'test_253.miz'),
    ids=('older version', '1.5.8', '2.5.2', '2.5.3')
)
def test_file(request, test_files_folder):
    yield Path(test_files_folder, request.param)


@pytest.fixture()
def latest_test_file(test_files_folder):
    yield Path(test_files_folder, 'test_253.miz').absolute()


@pytest.fixture()
def out_file(test_files_folder):
    yield Path(test_files_folder, 'TRG_KA50_EMFT.miz').absolute()


@pytest.fixture()
def bad_zip_file():
    yield Path(TEST_FILES_FOLDER.joinpath('bad_zip_file.miz')).absolute()


@pytest.fixture()
def missing_file():
    yield Path(TEST_FILES_FOLDER.joinpath('missing_files.miz')).absolute()


@pytest.fixture()
def duplicate_group_id():
    yield Path(TEST_FILES_FOLDER.joinpath('duplicate_group_id.miz')).absolute()


@pytest.fixture()
def dust_miz_file():
    yield Path(TEST_FILES_FOLDER.joinpath('test_dust.miz')).absolute()


@pytest.fixture()
def all_objects():
    yield Path(TEST_FILES_FOLDER.joinpath('all_objects.miz')).absolute()


@pytest.fixture(
    params=('TRMT_2.4.0.miz', 'SDCM_1.4.0.127_csar.miz'),
    ids=('TRMT_2.4.0', 'SDCM_1.4.0.127_csar')
)
def large_file(request):
    yield Path(TEST_FILES_FOLDER.joinpath(request.param)).absolute()


@pytest.fixture()
def radio_file():
    yield Path(TEST_FILES_FOLDER.joinpath('radios.miz')).absolute()


@pytest.fixture()
def test_files_folder():
    yield TEST_FILES_FOLDER


# @pytest.fixture(
#     params=('bad_zip_file.miz', 'missing_files.miz'),
#     ids=('bad_zip_file', 'missing_files'))
# def bad_files(request):
#     yield Path(TEST_FILES_FOLDER.joinpath(request.param))


@pytest.fixture(autouse=True)
def remove_out_file():
    """Removes OUT_FILE between tests"""
    path = Path(TEST_FILES_FOLDER.joinpath('TRG_KA50_EMFT.miz'))
    if path.exists():
        path.unlink()
    yield
    if path.exists():
        path.unlink()


with Miz(Path(TEST_FILES_FOLDER.joinpath('test_158.miz'))) as miz:
    DUMMY_MISSION = miz.mission


@pytest.fixture()
def mission() -> Mission:
    yield Mission(copy.deepcopy(DUMMY_MISSION.d), copy.deepcopy(DUMMY_MISSION.l10n))


# @pytest.fixture()
# def mission_dict():
#     yield copy.deepcopy(DUMMY_MISSION.d)


# @pytest.fixture()
# def mission_l10n():
#     yield copy.deepcopy(DUMMY_MISSION.l10n)


@pytest.fixture(params=list(Path(SLTP_TEST_FILE, 'pass').iterdir()))
def sltp_pass(request):
    yield request.param


@pytest.fixture(params=list(Path(SLTP_TEST_FILE, 'diff').iterdir()))
def sltp_diff(request):
    yield request.param


@pytest.fixture(params=list(Path(SLTP_TEST_FILE, 'long').iterdir()))
def sltp_long(request):
    yield request.param


@pytest.fixture(params=list(Path(SLTP_TEST_FILE, 'fail').iterdir()))
def sltp_fail(request):
    yield request.param
