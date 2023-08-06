# coding=utf-8


import pytest
from mockito import expect, mock, verify, verifyNoUnwantedInteractions, verifyStubbedInvocationsAreUsed, when

# noinspection PyProtectedMember
from elib_run._run import _run


@pytest.mark.parametrize(
    'mute',
    [True, False]
)
def test_exit(mute, caplog):
    caplog.set_level(10, 'elib_run.process')
    context = mock(
        {
            'mute': mute,
            'process_output_as_str': 'dummy_output',
            'process_logger': mock(),
        }
    )
    when(context.process_logger).debug(...)
    with pytest.raises(SystemExit):
        _run._exit(context)
    if mute:
        assert 'dummy_output' in caplog.text
    else:
        assert '' == caplog.text


@pytest.mark.parametrize('return_code', (0, 1))
@pytest.mark.parametrize('mute', (True, False))
@pytest.mark.parametrize('failure_ok', (True, False))
def test_check_error(return_code, mute, failure_ok, caplog):
    caplog.set_level(10)
    context = mock(
        {
            'return_code': return_code,
            'mute': mute,
            'result_buffer': '',
            'failure_ok': failure_ok,
            'cmd_as_string': 'dummy_cmd',
            'process_logger': mock(),
        }
    )
    when(_run)._exit(context)
    result = _run.check_error(context)
    if return_code is 0:
        if mute:
            expected_buffer = f': success: {return_code}'
        else:
            expected_buffer = f'{context.cmd_as_string}: success: {context.return_code}'
        assert expected_buffer in caplog.text
        assert result is 0
    else:
        if mute:
            expected_buffer = f': command failed: {context.return_code}'
        else:
            expected_buffer = f'{context.cmd_as_string}: command failed: {context.return_code}'
        assert expected_buffer in caplog.text
        assert repr(context) in caplog.text
        if not failure_ok:
            verify(_run)._exit(context)
        else:
            verify(_run, times=0)._exit(...)


@pytest.mark.parametrize(
    'filters',
    (None, ['some'], ['some', 'string'], 'some string')
)
def test_sanitize_filters(filters):
    result = _run._sanitize_filters(filters)
    if filters is None:
        assert result is None
    elif isinstance(filters, str):
        assert [filters] == result
    else:
        assert result is filters


@pytest.mark.parametrize(
    'filters',
    ([False], [None], [True], [1], [1.1], [['list']], [{'k': 'v'}], True, False, 1.1, 1, ('tuple',), {'k': 'v'})
)
def test_sanitize_filters_wrong_value(filters):
    with pytest.raises(TypeError):
        _run._sanitize_filters(filters)


def test_parse_exe_no_args():
    when(_run).find_executable(...).thenReturn('dummy')
    result = _run._parse_cmd('cmd')
    assert 'dummy', '' == result
    verifyStubbedInvocationsAreUsed()


def test_parse_exe_with_args():
    when(_run).find_executable(...).thenReturn('dummy')
    result = _run._parse_cmd('cmd')
    assert 'dummy', ['some', 'args'] == result
    verifyStubbedInvocationsAreUsed()


def test_parse_cmd_exe_not_found():
    when(_run).find_executable(...).thenReturn(None)
    with pytest.raises(_run.ExecutableNotFoundError):
        _run._parse_cmd('dummy')
    verifyStubbedInvocationsAreUsed()


@pytest.mark.parametrize(
    'mute', (True, False)
)
def test_run(mute):
    expect(_run.RunContext).start_process()
    expect(_run).monitor_running_process(...)
    expect(_run).check_error(...)
    _run.run('cmd', mute=mute)
    verifyNoUnwantedInteractions()
