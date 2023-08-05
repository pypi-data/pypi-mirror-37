# coding=utf-8
"""
Manages runners
"""
import logging
import pathlib
import shlex
import sys
import typing

import sarge

from elib_run._exc import ExecutableNotFoundError
from elib_run._find_exe import find_executable
from elib_run._run._monitor_running_process import monitor_running_process
from elib_run._run._run_context import RunContext

_DEFAULT_PROCESS_TIMEOUT = float(60)
_LOGGER_PROCESS = logging.getLogger('elib_run.process')


def _exit(context: RunContext):
    if context.mute:
        _LOGGER_PROCESS.error('process output:\n%s', context.process_output_as_str)
    sys.exit(context.return_code)


def check_error(context: RunContext) -> int:
    """
    Runs after a sub-process exits

    Checks the return code; if it is different than 0, then a few things happen:

        - if the process was muted ("mute" is True), the process output is printed anyway
        - if "failure_ok" is True (default), then a SystemExist exception is raised

    :param context: run context
    :type context: _RunContext
    :return: process return code
    :rtype: int
    """

    if context.return_code != 0:
        if context.mute:
            context.result_buffer += f': command failed: {context.return_code}'
        else:
            context.result_buffer += f'{context.cmd_as_string}: command failed: {context.return_code}'

        _LOGGER_PROCESS.error(context.result_buffer)
        _LOGGER_PROCESS.error(repr(context))

        if not context.failure_ok:
            _exit(context)
    else:
        if context.mute:
            context.result_buffer += f': success: {context.return_code}'
        else:
            context.result_buffer += f'{context.cmd_as_string}: success: {context.return_code}'
        _LOGGER_PROCESS.info(context.result_buffer)

    return context.return_code


def _sanitize_filters(filters: typing.Optional[typing.Union[typing.Iterable[str], str]]
                      ) -> typing.Optional[typing.Iterable[str]]:
    if filters and isinstance(filters, str):
        return [filters]
    if filters is not None:
        if not isinstance(filters, list):
            raise TypeError(f'expected a list, got {type(filters)} instead')
        for index, item in enumerate(filters):
            if not isinstance(item, str):
                raise TypeError(f'item at position {index} is not a string: {type(item)}')
    return filters


def _parse_cmd(cmd: str, *paths: str) -> typing.Tuple[pathlib.Path, typing.List[str]]:
    try:
        exe_name, args = cmd.split(' ', maxsplit=1)
    except ValueError:
        # cmd has no argument
        exe_name, args = cmd, ''
    exe_path: typing.Optional[pathlib.Path] = find_executable(exe_name, *paths)

    if not exe_path:
        raise ExecutableNotFoundError(exe_name)

    args_list = shlex.split(args)

    return exe_path, args_list


def run(cmd: str,
        *paths: str,
        cwd: str = '.',
        mute: bool = False,
        filters: typing.Optional[typing.Union[typing.Iterable[str], str]] = None,
        failure_ok: bool = False,
        timeout: float = _DEFAULT_PROCESS_TIMEOUT,
        ) -> typing.Tuple[str, int]:
    """
    Executes a command and returns the result

    Args:
        cmd: command to execute
        paths: paths to search executable in
        cwd: working directory (defaults to ".")
        mute: if true, output will not be printed
        filters: gives a list of partial strings to filter out from the output (stdout or stderr)
        failure_ok: if False (default), a return code different than 0 will exit the application
        timeout: sub-process timeout

    Returns: command output
    """

    filters = _sanitize_filters(filters)

    exe_path, args_list = _parse_cmd(cmd, *paths)

    context = RunContext(  # type: ignore
        exe_path=exe_path,
        capture=sarge.Capture(),
        failure_ok=failure_ok,
        mute=mute,
        args_list=args_list,
        paths=paths,
        cwd=cwd,
        timeout=timeout,
        filters=filters,
    )

    if mute:
        context.result_buffer += f'{context.cmd_as_string}'
    else:
        _LOGGER_PROCESS.info('%s: running', context.cmd_as_string)

    context.start_process()
    monitor_running_process(context)
    check_error(context)

    return context.process_output_as_str, context.return_code
