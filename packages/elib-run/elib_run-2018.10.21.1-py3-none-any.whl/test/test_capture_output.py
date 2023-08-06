# coding=utf-8

import string

import pytest
from hypothesis import given, strategies as st
from mockito import mock, verify, verifyNoUnwantedInteractions, verifyStubbedInvocationsAreUsed, when

# noinspection PyProtectedMember
from elib_run._run import _capture_output


@given(text=st.text(alphabet=string.printable))
def test_filter_line_raw(text):
    context = mock()
    context.filters = None
    assert _capture_output.filter_line(text, context) == text


@pytest.mark.parametrize(
    'text,filters,expected_return',
    (
        ['some random text', None, 'some random text'],
        ['some random text', ['.*some.*'], None],
        ['some random text', ['.*empty.*'], 'some random text'],
    )
)
def test_filter_line(text, filters, expected_return):
    assert isinstance(text, str)
    context = mock()
    context.filters = filters
    assert expected_return == _capture_output.filter_line(text, context)


def test_decode_and_filter():
    line_bytes = 'random string'.encode('utf8')
    context = mock({'filters': None, 'console_encoding': 'cp437'})
    result = _capture_output.decode_and_filter(line_bytes, context)
    assert 'random string' == result


def test_decode_and_filter_filtered():
    line_bytes = 'random string'.encode('utf8')
    context = mock({'filters': ['random.*'], 'console_encoding': 'cp437'})
    result = _capture_output.decode_and_filter(line_bytes, context)
    assert result is None


def _dummy_context():
    return mock(
        {
            'capture': mock(),
            'filters': None,
            'mute': False,
            'process_output_chunks': [],
            'console_encoding': 'utf8',
            'process_logger': mock(),
        }
    )


def test_capture_simple(caplog):
    caplog.set_level(10, 'elib_run.process')
    context = _dummy_context()
    when(context.capture).readline(block=False).thenReturn(b'random string').thenReturn(None)
    _capture_output.capture_output_from_running_process(context)
    verifyNoUnwantedInteractions()
    verifyStubbedInvocationsAreUsed()
    assert ['random string'] == context.process_output_chunks
    assert 'random string' in caplog.text


def test_capture_filtered():
    context = _dummy_context()
    context.filters = ['random.*']
    when(context.capture).readline(block=False).thenReturn(b'random string').thenReturn(None)
    when(context.process_logger).debug(...)
    _capture_output.capture_output_from_running_process(context)
    verify(context.process_logger, times=0).debug(...)
    verifyNoUnwantedInteractions()
    verifyStubbedInvocationsAreUsed()
    assert [] == context.process_output_chunks


def test_capture_muted():
    context = _dummy_context()
    context.mute = True
    when(context.capture).readline(block=False).thenReturn(b'random string').thenReturn(None)
    when(context.process_logger).debug(...)
    _capture_output.capture_output_from_running_process(context)
    verify(context.process_logger, times=0).debug(...)
    verifyNoUnwantedInteractions()
    verifyStubbedInvocationsAreUsed()
    assert ['random string'] == context.process_output_chunks
