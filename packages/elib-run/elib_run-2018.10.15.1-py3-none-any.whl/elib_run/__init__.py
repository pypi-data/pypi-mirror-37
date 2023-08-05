# coding=utf-8
"""
Top-level package for elib_run.
"""

from pkg_resources import DistributionNotFound, get_distribution

# noinspection PyProtectedMember
from elib_run._run._run import run
from ._exc import ELIBRunError, ExecutableNotFoundError
from ._find_exe import find_executable

try:
    __version__ = get_distribution('elib_run').version
except DistributionNotFound:  # pragma: no cover
    # package is not installed
    __version__ = 'not installed'

__author__ = """etcher"""
__email__ = 'etcher@daribouca.net'

__all__ = ['run', 'find_executable', 'ELIBRunError', 'ExecutableNotFoundError']


# pylint: disable=unused-argument,missing-docstring
def register_console_hooks(*args, **kwargs):  # pragma: no cover
    import warnings
    warnings.warn('console hooks registration are not supported anymore', PendingDeprecationWarning)
