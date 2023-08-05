# coding=utf-8

import sys
from pathlib import Path

import pytest

# noinspection PyProtectedMember
from elib_run import _find_exe


@pytest.mark.filterwarnings('ignore::UserWarning')
def test_find_executable():
    python = _find_exe.find_executable('python')
    assert _find_exe.find_executable('python.exe') == python
    assert _find_exe.find_executable('python', f'{sys.prefix}/Scripts') == python
    assert _find_exe.find_executable('__sure__not__') is None


@pytest.mark.filterwarnings('ignore::UserWarning')
def test_context():
    assert _find_exe.find_executable('__sure__not__') is None
    _find_exe._KNOWN_EXECUTABLES['__sure__not__.exe'] = 'ok'
    assert _find_exe.find_executable('__sure__not__') == 'ok'


@pytest.mark.filterwarnings('ignore::UserWarning')
def test_paths():
    assert _find_exe.find_executable('python')
    assert _find_exe.find_executable('python', '.')
    _find_exe._KNOWN_EXECUTABLES = {}
    assert _find_exe.find_executable('python', '.') is None


@pytest.mark.filterwarnings('ignore::UserWarning')
def test_direct_find():
    exe = Path('test.exe')
    exe.touch()
    assert exe.absolute() == _find_exe.find_executable('test')
