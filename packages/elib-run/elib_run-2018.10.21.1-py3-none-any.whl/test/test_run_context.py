# coding=utf-8


import pathlib
import time

import faker
import pytest
import sarge
from mockito import (
    mock, verify, verifyNoUnwantedInteractions, verifyStubbedInvocationsAreUsed, verifyZeroInteractions, when,
)

# noinspection PyProtectedMember
from elib_run._run import _run, _run_context


@pytest.fixture()
def dummy_kwargs() -> dict:
    yield dict(
        exe_path=pathlib.Path('./test.exe'),
        capture=sarge.Capture(),
        failure_ok=True,
        mute=True,
        args_list=['some', 'args'],
        paths=['.'],
        cwd='.',
        timeout=10.0,
        filters=['some', 'string'],
    )


@pytest.mark.parametrize(
    'arg_name,wrong_values',
    (
        ('exe_path', ('string', 1, False, True, None, 1.1, ['list'], {'k': 'v'}, sarge.Capture())),
        ('capture', ('string', 1, False, True, None, 1.1, ['list'], {'k': 'v'}, pathlib.Path('.'))),
        ('failure_ok', ('string', 1, None, 1.1, ['list'], {'k': 'v'}, pathlib.Path('.'), sarge.Capture())),
        ('mute', ('string', 1, None, 1.1, ['list'], {'k': 'v'}, pathlib.Path('.'), sarge.Capture())),
        ('cwd', (1, None, True, False, 1.1, {'k': 'v'}, pathlib.Path('.'), sarge.Capture())),
        ('timeout', (None, True, False, 'string', {'k': 'v'}, pathlib.Path('.'), sarge.Capture())),
        ('args_list', ('string', 1, 1.1, {'k': 'v'}, pathlib.Path('.'), sarge.Capture())),
        ('paths', ('string', 1, 1.1, {'k': 'v'}, pathlib.Path('.'), sarge.Capture())),
        ('filters', ('string', 1, 1.1, {'k': 'v'}, pathlib.Path('.'), sarge.Capture())),
    )
)
def test_wrong_init(arg_name, wrong_values, dummy_kwargs):
    for wrong_value in wrong_values:
        wrong_kwargs = dummy_kwargs.copy()
        wrong_kwargs[arg_name] = wrong_value
        with pytest.raises(TypeError):
            _run_context.RunContext(**wrong_kwargs)


@pytest.mark.parametrize(
    'arg_name',
    ('args_list', 'paths', 'filters')
)
@pytest.mark.parametrize(
    'wrong_value',
    (
        [1, 2, 3, 4],
        [pathlib.Path('.'), pathlib.Path('.'), pathlib.Path('.')],
        [{'k': 'v'}, {'k': 'v'}, {'k': 'v'}],
        [None, None, None],
        [True, True, False],
        [1.0, 2.0, 30.3],
    )
)
def test_wrong_init_lists_of_string(arg_name, wrong_value, dummy_kwargs):
    wrong_kwargs = dummy_kwargs.copy()
    wrong_kwargs[arg_name] = wrong_value
    with pytest.raises(TypeError):
        _run_context.RunContext(**wrong_kwargs)


@pytest.mark.parametrize(
    'optional_arg_name',
    (None, 'args_list', 'filters', 'paths')
)
def test_valid_init(dummy_kwargs, optional_arg_name):
    correct_kwargs = dummy_kwargs.copy()
    if optional_arg_name:
        correct_kwargs[optional_arg_name] = []
    _run_context.RunContext(**correct_kwargs)


def test_start_process(dummy_kwargs):
    command = mock()
    when(command).run(async_=True)
    context = _run_context.RunContext(**dummy_kwargs)
    setattr(context, '_command', command)
    assert context.start_time == 0
    verifyZeroInteractions()
    context.start_process()
    assert context.start_time != 0
    verifyStubbedInvocationsAreUsed()
    verifyNoUnwantedInteractions()


def test_process_timed_out(dummy_kwargs):
    context = _run_context.RunContext(**dummy_kwargs)
    setattr(context, '_started', True)
    assert context.process_timed_out()


def test_process_not_timed_out(dummy_kwargs):
    context = _run_context.RunContext(**dummy_kwargs)
    setattr(context, '_started', True)
    context.start_time = time.monotonic()
    assert not context.process_timed_out()


def test_process_timed_out_process_not_started(dummy_kwargs):
    context = _run_context.RunContext(**dummy_kwargs)
    with pytest.raises(RuntimeError):
        assert context.process_timed_out()


def test_process_finished(dummy_kwargs):
    command = mock()
    when(command).poll().thenReturn(None).thenReturn(0)
    context = _run_context.RunContext(**dummy_kwargs)
    setattr(context, '_command', command)
    assert not context.process_finished()
    assert context.process_finished()
    verifyNoUnwantedInteractions()
    verifyStubbedInvocationsAreUsed()


@pytest.mark.parametrize(
    'fake_output',
    (faker.Faker().paragraphs(nb=3, ext_word_list=None) for _ in range(10))
)
def test_process_output_as_str(fake_output, dummy_kwargs):
    context = _run_context.RunContext(**dummy_kwargs)
    expected_output_list = [
        '\n'.join(fake_output) for _ in range(10)
    ]
    context.process_output_chunks = list(expected_output_list)
    assert '\n'.join(expected_output_list) == context.process_output_as_str


@pytest.mark.parametrize(
    'test_file_name',
    (faker.Faker().file_name(category=None, extension=None) for _ in range(10))
)
def test_exe_path_as_str(dummy_kwargs, test_file_name):
    test_file_path = pathlib.Path(test_file_name)
    dummy_kwargs['exe_path'] = test_file_path
    context = _run_context.RunContext(**dummy_kwargs)
    assert test_file_path == context.exe_path
    assert isinstance(context.exe_path, pathlib.Path)
    assert str(test_file_path.absolute()) == context.exe_path_as_str
    assert isinstance(context.exe_path_as_str, str)


@pytest.mark.parametrize(
    'test_cwd',
    (faker.Faker().file_name(category=None, extension=None) for _ in range(10))
)
def test_cwd_path_as_str(dummy_kwargs, test_cwd):
    test_cwd_path = pathlib.Path(test_cwd)
    dummy_kwargs['cwd'] = test_cwd
    context = _run_context.RunContext(**dummy_kwargs)
    assert test_cwd == context.cwd
    assert isinstance(context.cwd, str)
    assert str(test_cwd_path.absolute()) == context.absolute_cwd_as_str
    assert isinstance(context.absolute_cwd_as_str, str)


@pytest.mark.parametrize(
    'exe_name',
    (faker.Faker().file_name(category=None, extension=None) for _ in range(10))
)
@pytest.mark.parametrize(
    'arg_list',
    (faker.Faker().words(nb=3, ext_word_list=None) for _ in range(10))
)
def test_cwd_path_as_str(dummy_kwargs, exe_name, arg_list):
    exe_path = pathlib.Path(exe_name).absolute()
    dummy_kwargs['exe_path'] = exe_path
    dummy_kwargs['args_list'] = arg_list
    context = _run_context.RunContext(**dummy_kwargs)
    assert context.exe_path == exe_path
    assert context.args_list == arg_list
    exe_path_as_str = str(exe_path)
    arg_list_as_str = ' '.join(arg_list)
    cmd_as_str = ' '.join((exe_path_as_str, arg_list_as_str))
    assert f'"{cmd_as_str}" in "{context.absolute_cwd_as_str}"' == context.cmd_as_string


@pytest.mark.parametrize(
    'exe_name',
    (faker.Faker().file_name(category=None, extension=None) for _ in range(10))
)
def test_cwd_path_as_str_no_args(dummy_kwargs, exe_name):
    exe_path = pathlib.Path(exe_name).absolute()
    dummy_kwargs['exe_path'] = exe_path
    dummy_kwargs['args_list'] = []
    context = _run_context.RunContext(**dummy_kwargs)
    assert context.exe_path == exe_path
    exe_path_as_str = str(exe_path)
    assert f'"{exe_path_as_str}" in "{context.absolute_cwd_as_str}"' == context.cmd_as_string


@pytest.mark.parametrize(
    'exe_name',
    (faker.Faker().file_name(category=None, extension=None) for _ in range(10))
)
def test_exe_short_name(dummy_kwargs, exe_name):
    exe_path = pathlib.Path(exe_name).absolute()
    dummy_kwargs['exe_path'] = exe_path
    context = _run_context.RunContext(**dummy_kwargs)
    assert exe_name == context.exe_short_name


def test_command(dummy_kwargs):
    context = _run.RunContext(**dummy_kwargs)
    command = mock()
    when(sarge).Command(
        [context.exe_path_as_str] + context.args_list,
        stdout=context.capture,
        stderr=context.capture,
        shell=False,
        cwd=context.cwd,
    ).thenReturn(command)
    for _ in range(10):
        assert command is context.command
        assert getattr(context, '_command') is command
    verify(sarge).Command(
        [context.exe_path_as_str] + context.args_list,
        stdout=context.capture,
        stderr=context.capture,
        shell=False,
        cwd=context.cwd,
    )
