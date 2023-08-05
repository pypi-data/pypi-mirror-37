﻿# coding=utf-8
"""
Manages MIZ files
"""
import logging
import os
import shutil
import tempfile
import typing
from filecmp import dircmp
from pathlib import Path
from zipfile import BadZipFile, ZipFile

from elib_miz.dummy_miz import dummy_miz
from elib_miz.mission import Mission
from elib_miz.sltp import SLTP

LOGGER = logging.getLogger('elib.miz')

ENCODING = 'iso8859_15'


# pylint: disable=too-many-instance-attributes
class Miz:
    """
    Manage MIZ files
    """

    def __init__(self,
                 path_to_miz_file: typing.Union[str, Path],
                 temp_dir: typing.Union[str, Path] = None,
                 keep_temp_dir: bool = False,
                 overwrite: bool = False
                 ) -> None:

        _miz_path = Path(path_to_miz_file).absolute()
        if not _miz_path.exists():
            raise FileNotFoundError(_miz_path)
        if not _miz_path.is_file():
            raise TypeError(f'not a file: {_miz_path}')

        self.miz_path = _miz_path

        if self.miz_path.suffix != '.miz':
            raise ValueError(f'MIZ file should end with the ".miz" extension: {self.miz_path}')

        if temp_dir is not None:
            raise PendingDeprecationWarning()

        self.keep_temp_dir = keep_temp_dir

        self.overwrite = overwrite

        self.temp_dir = Path(tempfile.mkdtemp('EMFT_'))
        LOGGER.debug('temporary directory: %s', self.temp_dir)

        self.zip_content: typing.Optional[typing.List[str]] = None
        self._mission: typing.Optional[Mission] = None
        self._mission_qual = None
        self._l10n = None
        self._l10n_qual = None
        self._map_res = None
        self._map_res_qual = None
        self._resources: set = set()

    def __enter__(self):
        LOGGER.debug('instantiating new Mission object as a context')
        self.unzip(self.overwrite)
        self.decode()
        return self

    def __exit__(self, exc_type, exc_val, _):
        if exc_type:
            LOGGER.error('there were error with this mission, keeping temp dir at "%s"', self.temp_dir)
            LOGGER.error('%s\n%s', exc_type, exc_val)
            return False

        LOGGER.debug('closing Mission object context')
        if not self.keep_temp_dir:
            LOGGER.debug('removing temp dir: %s', self.temp_dir)
            self._remove_temp_dir()
        return True

    @property
    def mission_file(self) -> Path:
        """

        Returns: mission file path

        """
        return self.temp_dir.joinpath('mission')

    @property
    def dictionary_file(self) -> Path:
        """

        Returns: l10n file path

        """
        return self.temp_dir.joinpath('l10n', 'DEFAULT', 'dictionary')

    @property
    def map_res_file(self) -> Path:
        """

        Returns: resource map file path

        """
        return self.temp_dir.joinpath('l10n', 'DEFAULT', 'mapResource')

    @property
    def mission(self) -> Mission:
        """

        Returns: mission

        """
        if self._mission is None:
            raise RuntimeError()
        return self._mission

    @mission.setter
    def mission(self, value: Mission):
        if not isinstance(value, Mission):
            raise TypeError(f'expected a "Mission" object, got: {type(value)}')
        self._mission = value

    @property
    def l10n(self) -> dict:
        """

        Returns: l10n dictionary

        """
        if self._l10n is None:
            raise RuntimeError()
        return self._l10n

    @property
    def map_res(self) -> dict:
        """

        Returns: map resources dictionary

        """
        if self._map_res is None:
            raise RuntimeError()
        return self._map_res

    @property
    def resources(self):
        """

        Returns: resources available to this mission

        """
        return self._resources

    @staticmethod
    def _do_reorder(miz_file_path, skip_options_file, target_dir_path):

        with Miz(miz_file_path, overwrite=True) as miz_:

            def mirror_dir(src: Path, dst: Path):
                """
                Propagates difference between the original lua tables and the re-ordered one

                Args:
                    src: source folder
                    dst: destination folder
                """
                LOGGER.debug('mirroring: %s -> %s', src, dst)

                LOGGER.debug('comparing directories')
                diff_ = dircmp(str(src), str(dst), ignore)

                diff_list = diff_.left_only + diff_.diff_files
                LOGGER.debug('differences: %s', diff_list)

                for __diff in diff_list:
                    source = Path(diff_.left, __diff)
                    target = Path(diff_.right, __diff)
                    LOGGER.debug('looking at: %s', __diff)
                    if source.is_dir():
                        LOGGER.debug('isdir: %s', __diff)
                        if not target.exists():
                            LOGGER.debug('creating: %s', __diff)
                            target.mkdir()
                        mirror_dir(source, target)
                    else:
                        LOGGER.debug('copying: %s', __diff)
                        shutil.copy2(str(source), diff_.right)
                for sub in diff_.subdirs.values():

                    mirror_dir(Path(sub.left), Path(sub.right))

            # pylint: disable=protected-access
            miz_._encode()

            if skip_options_file:
                ignore = ['options']
            else:
                ignore = []

            mirror_dir(Path(miz_.temp_dir), target_dir_path)

    @staticmethod
    def reorder(miz_file_path: typing.Union[str, Path],
                target_dir: typing.Union[str, Path],
                skip_options_file: bool,
                ):
        """
        Re-orders a miz file into a folder (flattened)

        Args:
            miz_file_path: source miz file
            target_dir: folder to flatten the content into
            skip_options_file: do not re-order option file

        """

        miz_file_path = Path(miz_file_path).absolute()
        if not miz_file_path.exists():
            raise FileNotFoundError(miz_file_path)
        if not miz_file_path.is_file():
            raise ValueError(f'not a file: {miz_file_path}')

        target_dir_path = Path(target_dir).absolute()
        if not target_dir_path.exists():
            target_dir_path.mkdir(parents=True)
        else:
            if not target_dir_path.is_dir():
                raise ValueError(f'not a directory: {target_dir_path}')

        LOGGER.debug('re-ordering miz file: %s', miz_file_path)
        LOGGER.debug('destination folder: %s', target_dir)
        LOGGER.debug('%s option file', "skipping" if skip_options_file else "including")

        if not target_dir_path.exists():
            LOGGER.debug('creating directory %s', target_dir_path)
            target_dir_path.mkdir(exist_ok=True)

        Miz._do_reorder(miz_file_path, skip_options_file, target_dir_path)

    def decode(self):
        """Decodes the mission files into dictionaries"""

        LOGGER.debug('decoding lua tables')

        if not self.zip_content:
            self.unzip()

        LOGGER.debug('reading map resource file')
        with open(str(self.map_res_file), encoding=ENCODING) as stream:
            self._map_res, self._map_res_qual = SLTP().decode(stream.read())

        LOGGER.debug('reading l10n file')
        with open(str(self.dictionary_file), encoding=ENCODING) as stream:
            self._l10n, self._l10n_qual = SLTP().decode(stream.read())

        LOGGER.debug('reading mission file')
        with open(str(self.mission_file), encoding=ENCODING) as stream:
            mission_data, self._mission_qual = SLTP().decode(stream.read())
            self._mission = Mission(mission_data, self._l10n)

        LOGGER.debug('gathering resources')
        for file in Path(self.temp_dir, 'l10n', 'DEFAULT').iterdir():
            if file.name in ('dictionary', 'mapResource'):
                continue
            LOGGER.debug('found resource: %s', file.name)
            self._resources.add(file.name)

        LOGGER.debug('decoding done')

    def _encode(self):

        LOGGER.debug('encoding lua tables')

        LOGGER.debug('encoding map resource')
        with open(str(self.map_res_file), mode='w', encoding=ENCODING) as stream:
            stream.write(SLTP().encode(self._map_res, self._map_res_qual))

        LOGGER.debug('encoding l10n dictionary')
        with open(str(self.dictionary_file), mode='w', encoding=ENCODING) as stream:
            stream.write(SLTP().encode(self.l10n, self._l10n_qual))

        LOGGER.debug('encoding mission dictionary')
        with open(str(self.mission_file), mode='w', encoding=ENCODING) as stream:
            stream.write(SLTP().encode(self.mission.d, self._mission_qual))

        LOGGER.debug('encoding done')

    def _check_extracted_content(self):

        for filename in self.zip_content:
            path = Path(self.temp_dir.joinpath(filename))
            if not path.exists():
                raise FileNotFoundError(str(path))

    def _extract_files_from_zip(self, zip_file):

        for item in zip_file.infolist():  # not using ZipFile.extractall() for security reasons

            LOGGER.debug('unzipping item: %s', item.filename)

            try:
                zip_file.extract(item, str(self.temp_dir))
            except:  # noqa: E722
                LOGGER.error('failed to extract archive member: %s', item.filename)
                raise

    def _remove_temp_dir(self):
        shutil.rmtree(str(self.temp_dir))

    def unzip(self, overwrite: bool = False):
        """
        Flattens a MIZ file into the temp dir

        Args:
            overwrite: allow overwriting exiting files

        """

        if self.zip_content and not overwrite:
            raise FileExistsError(str(self.temp_dir))

        LOGGER.debug('unzipping miz to temp dir')

        try:

            with ZipFile(str(self.miz_path)) as zip_file:

                LOGGER.debug('reading infolist')

                self.zip_content = [f.filename for f in zip_file.infolist()]

                self._extract_files_from_zip(zip_file)

        except BadZipFile:
            raise BadZipFile(str(self.miz_path))

        except:  # noqa: E722
            LOGGER.exception('error while unzipping miz file: %s', self.miz_path)
            raise

        LOGGER.debug('checking miz content')

        # noinspection PyTypeChecker
        for miz_item in ['mission', 'options', 'warehouses', 'l10n/DEFAULT/dictionary', 'l10n/DEFAULT/mapResource']:
            if not Path(self.temp_dir.joinpath(miz_item)).exists():
                LOGGER.error('missing file in miz: %s', miz_item)
                raise FileNotFoundError(miz_item)

        self._check_extracted_content()

        LOGGER.debug('all files have been found, miz successfully unzipped')

    def zip(self, destination: typing.Union[str, Path] = None, encode: bool = True) -> str:
        """
        Write mission, dictionary etc. to a MIZ file

        :param destination: target MIZ file (if none, defaults to source MIZ + "_EMIZ"
        :type destination: str or Path
        :param encode: if True, re-encode the lua tables
        :type encode: bool
        :return: destination file
        :rtype: str
        """
        if encode:
            self._encode()

        if destination is None:
            destination_path = self.miz_path.parent.joinpath(f'{self.miz_path.stem}_EMIZ.miz')
        else:
            destination_path = Path(destination).absolute()
            if destination_path.exists() and not destination_path.is_file():
                raise ValueError(f'not a file: {destination_path}')

        LOGGER.debug('zipping mission to: %s', destination_path)

        destination_path.write_bytes(dummy_miz)

        with ZipFile(str(destination_path), mode='w', compression=8) as zip_file:

            for root, _, items in os.walk(self.temp_dir.absolute()):
                for item in items:
                    item_abs_path = Path(root, item).absolute()
                    item_rel_path = Path(item_abs_path).relative_to(self.temp_dir)
                    zip_file.write(item_abs_path, arcname=item_rel_path)

        return str(destination_path)
