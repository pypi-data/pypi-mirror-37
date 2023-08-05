# coding=utf-8

import pathlib

import sarge
from mockito import patch, verifyStubbedInvocationsAreUsed, when

from elib_run._run import _run


def test_successful_run(caplog):
    caplog.set_level(20)

    def _fake_monitor(context):
        context.return_code = 0

    when(sarge.Command).run(...)
    test_exe = pathlib.Path('./test.exe')
    when(_run).find_executable('test').thenReturn(test_exe)
    patch(_run.monitor_running_process, _fake_monitor)
    _run.run('test')
    verifyStubbedInvocationsAreUsed()
    assert [
        ('elib_run.process', 20, f'"{test_exe.absolute()}" in "{test_exe.parent.absolute()}": running'),
        ('elib_run.process', 20, f'"{test_exe.absolute()}" in "{test_exe.parent.absolute()}": success: 0'),
    ] == caplog.record_tuples
