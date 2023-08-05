# coding=utf-8
# coding=utf-8
"""
Finds an executable on the system
"""

import logging
import shutil
import typing
from pathlib import Path

_KNOWN_EXECUTABLES: typing.Dict[str, Path] = {}

_LOGGER = logging.getLogger('elib_run')


def find_executable(executable: str) -> typing.Optional[Path]:
    """
    Finds a given executable in the path

    :param executable: executable name
    :type executable: str
    :return: executable path
    :rtype: Path
    """
    if not executable.endswith('.exe'):
        executable = f'{executable}.exe'

    if executable in _KNOWN_EXECUTABLES:
        return _KNOWN_EXECUTABLES[executable]

    _found_path = shutil.which(executable)

    if _found_path is None:
        _LOGGER.error('%s -> not found', executable)
        return None

    _exe_path = Path(_found_path.lower()).absolute()

    _KNOWN_EXECUTABLES[executable] = _exe_path
    _LOGGER.info('%s -> %s', executable, str(_exe_path))

    return _exe_path
