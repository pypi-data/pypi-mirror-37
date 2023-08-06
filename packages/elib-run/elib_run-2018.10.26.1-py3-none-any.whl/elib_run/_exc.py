# coding=utf-8
"""
Exceptions for the elib_run package
"""
import typing


class ELIBRunError(Exception):
    """Base exception for the elib_run package"""


class ExecutableNotFoundError(ELIBRunError):
    """Raised when an executable is not found"""

    def __init__(self, exe_name: str, msg: typing.Optional[str] = None) -> None:
        self.exe_name = exe_name
        super(ExecutableNotFoundError, self).__init__(f'executable not found: {exe_name} ({msg})')


class ProcessTimeoutError(ELIBRunError):
    """Raised when a process runs for longer than a given timeout"""

    def __init__(self, exe_name: str, timeout: float, msg: typing.Optional[str] = None) -> None:
        self.exe_name = exe_name
        super(ProcessTimeoutError, self).__init__(
            f'process timeout: {exe_name} ran for more than {timeout} seconds ({msg})'
        )
