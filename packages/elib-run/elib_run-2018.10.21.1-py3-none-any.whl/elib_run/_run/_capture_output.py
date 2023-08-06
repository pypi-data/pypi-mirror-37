# coding=utf-8
"""
Responsible for reading and parsing output from a running sub-process
"""
import logging
import re
import typing

# noinspection PyProtectedMember
from elib_run._run._run_context import RunContext

_LOGGER_PROCESS = logging.getLogger('elib_run.process')


def filter_line(line: str, context: RunContext) -> typing.Optional[str]:
    """
    Filters out lines that match a given regex

    :param line: line to filter
    :type line: str
    :param context: run context
    :type context: _RunContext
    :return: line if it doesn't match the filter
    :rtype: optional str
    """
    if context.filters is not None:
        for filter_ in context.filters:
            if re.match(filter_, line):
                return None
    return line


def decode_and_filter(line: bytes, context: RunContext) -> typing.Optional[str]:
    """
    Decodes a line that was captured from the running process using a given encoding (defaults to UTF8)

    Runs that line into the filters, and output the decoded line back if no filter catches it.

    :param line: line to parse
    :type line: str
    :param context: run context
    :type context: RunContext
    :return: optional line
    :rtype: str
    """
    line_str: str = line.decode(context.console_encoding)
    filtered_line: typing.Optional[str] = filter_line(line_str, context)
    if filtered_line:
        return filtered_line.rstrip()

    return None


def capture_output_from_running_process(context: RunContext) -> None:
    """
    Parses output from a running sub-process

    Decodes and filters the process output line by line, buffering it

    If "mute" is False, sends the output back in real time

    :param context: run context
    :type context: _RunContext
    """
    # Get the raw output one line at a time
    _output = context.capture.readline(block=False)

    if _output:

        line = decode_and_filter(_output, context)

        if line:
            if not context.mute:

                # Print in real time
                _LOGGER_PROCESS.debug(line)

            # Buffer the line
            context.process_output_chunks.append(line)

        # Get additional output if any
        return capture_output_from_running_process(context)

    return None
