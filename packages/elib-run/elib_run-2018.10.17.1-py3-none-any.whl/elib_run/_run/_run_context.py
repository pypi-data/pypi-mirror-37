# coding=utf-8
"""
Dummy dataclass context for a sub-process run
"""
import pathlib
import time
import typing

# noinspection PyCompatibility
import dataclasses
import sarge


@dataclasses.dataclass
class RunContext:
    """
    Dummy dataclass context for a sub-process run
    """
    exe_path: pathlib.Path
    capture: sarge.Capture
    failure_ok: bool
    mute: bool
    args_list: typing.List[str]
    paths: typing.Optional[typing.Iterable[str]]
    cwd: str
    timeout: float
    process_output_chunks: typing.List[str] = dataclasses.field(default_factory=list, repr=False)
    result_buffer: str = dataclasses.field(default='', repr=False)
    filters: typing.Optional[typing.Iterable[str]] = None
    return_code: int = -1
    start_time: float = 0
    console_encoding: str = 'utf8'

    def _check_capture(self):
        if not isinstance(self.capture, sarge.Capture):
            raise TypeError(f'expected a sarge.Capture, got "{type(self.capture)}"')

    def _check_exe_path(self):
        if not isinstance(self.exe_path, pathlib.Path):
            raise TypeError(f'expected a pathlib.Path, got "{type(self.exe_path)}"')

    def _check_mute(self):
        if not isinstance(self.mute, bool):
            raise TypeError(f'expected a bool, got "{type(self.mute)}"')

    def _check_failure_ok(self):
        if not isinstance(self.failure_ok, bool):
            raise TypeError(f'expected a bool, got "{type(self.failure_ok)}"')

    def _check_paths(self):
        if self.paths:
            if not isinstance(self.paths, list):
                raise TypeError(f'expected a list, got "{type(self.paths)}"')
            for index, path in enumerate(self.paths):
                if not isinstance(path, str):
                    raise TypeError(f'expected a string, got "{type(path)}" at index {index}')

    def _check_cwd(self):
        if not isinstance(self.cwd, str):
            raise TypeError(f'expected a string, got "{type(self.cwd)}"')

    def _check_timeout(self):
        if not isinstance(self.timeout, (float, int)) or isinstance(self.timeout, bool):
            raise TypeError(f'expected a float, got "{type(self.timeout)}"')

    def _check_filters(self):
        if self.filters:
            if not isinstance(self.filters, list):
                raise TypeError(f'expected a list, got "{type(self.filters)}"')
            for index, filter_ in enumerate(self.filters):
                if not isinstance(filter_, str):
                    raise TypeError(f'expected a string, got "{type(filter_)}" at index {index}')

    def _check_args_list(self):
        if self.args_list:
            if not isinstance(self.args_list, list):
                raise TypeError(f'expected a list, got "{type(self.args_list)}"')
            for index, arg in enumerate(self.args_list):
                if not isinstance(arg, str):
                    raise TypeError(f'expected a string, got "{type(arg)}" at index {index}')

    def __post_init__(self):
        self._check_capture()
        self._check_exe_path()
        self._check_mute()
        self._check_failure_ok()
        self._check_paths()
        self._check_cwd()
        self._check_timeout()
        self._check_filters()
        self._check_args_list()

    def start_process(self) -> None:
        """
        Starts the process defined by this context
        """
        setattr(self, '_started', True)
        self.start_time = time.monotonic()
        self.command.run(async_=True)

    @property
    def started(self) -> bool:
        """
        :return: True if process has been started
        :rtype: bool
        """
        return getattr(self, '_started', False)

    def process_timed_out(self) -> bool:
        """
        :return: True if the process timed out
        :rtype: bool
        """
        if not self.started:
            raise RuntimeError('process not started')
        return time.monotonic() - self.start_time > self.timeout

    def process_finished(self) -> bool:
        """
        :return: True if a given process is done running
        :rtype: bool
        """
        return self.command.poll() is not None

    @property
    def process_output_as_str(self) -> str:
        """
        Returns process output so far

        :return: process output
        :rtype: str
        """
        return '\n'.join(self.process_output_chunks)

    @property
    def exe_path_as_str(self) -> str:
        """
        Returns executable path as a string

        :return: executable path
        :rtype: str
        """
        return str(self.exe_path.absolute())

    @property
    def absolute_cwd_as_str(self) -> str:
        """
        :return: absolute working dir
        :rtype: str
        """
        return str(pathlib.Path(self.cwd).absolute())

    @property
    def cmd_as_string(self) -> str:
        """
        Returns a concatenation of executable & args as a string

        :return: command
        :rtype: str
        """
        cmd = self.exe_path_as_str + (' ' + ' '.join(self.args_list) if self.args_list else '')
        return f'"{cmd}" in "{self.absolute_cwd_as_str}"'

    @property
    def exe_short_name(self) -> str:
        """
        Returns executable short name

        :return: executable short name
        :rtype: str
        """
        return self.exe_path.name

    @property
    def command(self) -> sarge.Command:
        """
        Returns sarge.Command instance, creating it if necessary

        :return: sarge.Command object
        :rtype: sarge.Command
        """
        if not hasattr(self, '_command'):
            command = sarge.Command(
                [self.exe_path_as_str] + self.args_list,
                stdout=self.capture,
                stderr=self.capture,
                shell=False,
                cwd=self.cwd,
            )
            setattr(self, '_command', command)
        return getattr(self, '_command')
