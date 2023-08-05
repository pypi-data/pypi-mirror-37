# coding=utf-8

import pytest
from mockito import mock, verify, when

# noinspection PyProtectedMember
from elib_run._run import _monitor_running_process


def test_monitor_running_process_poll():
    context = mock()
    context.command = mock({'returncode': 0})
    when(_monitor_running_process).capture_output_from_running_process(context)
    when(context).process_finished().thenReturn(True)
    when(context).process_timed_out()
    _monitor_running_process.monitor_running_process(context)
    assert 0 is context.return_code
    verify(_monitor_running_process)
    when(context).process_finished()
    verify(context, times=0).process_timed_out()


def test_monitor_running_process_break():
    context = mock()
    context.command = mock({'returncode': 0})
    when(_monitor_running_process).capture_output_from_running_process(context)
    when(context).process_finished().thenReturn(False).thenReturn(False).thenReturn(True)
    when(context).process_timed_out().thenReturn(False)
    _monitor_running_process.monitor_running_process(context)
    assert 0 is context.return_code
    verify(_monitor_running_process)
    when(context).process_finished()
    verify(context, times=2).process_timed_out()


def test_monitor_running_process_timeout():
    context = mock()
    context.command = mock({'returncode': 0})
    when(_monitor_running_process).capture_output_from_running_process(context)
    when(context).process_finished().thenReturn(False)
    when(context).process_timed_out().thenReturn(True)
    with pytest.raises(_monitor_running_process.ProcessTimeoutError):
        _monitor_running_process.monitor_running_process(context)
    assert -1 is context.return_code
    verify(_monitor_running_process)
    when(context).process_finished()
    verify(context).process_timed_out()
