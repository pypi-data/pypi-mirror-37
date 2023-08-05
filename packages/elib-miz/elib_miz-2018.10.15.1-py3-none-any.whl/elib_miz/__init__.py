# coding=utf-8
"""
Top-level package for elib_miz.
"""
# pylint: disable=wrong-import-position

import logging

from pkg_resources import DistributionNotFound, get_distribution

try:
    __version__ = get_distribution('elib_miz').version
except DistributionNotFound:  # pragma: no cover
    # package is not installed
    __version__ = 'not installed'

__author__ = """etcher"""
__email__ = 'etcher@daribouca.net'

LOGGER: logging.Logger = logging.getLogger('elib.miz')

from .mission import Mission
from .miz import Miz
from .static import Theater
from .mission_time import MissionTime
from . import exc

__all__ = ['Mission', 'Miz', 'Theater', 'MissionTime', 'LOGGER', 'exc']
