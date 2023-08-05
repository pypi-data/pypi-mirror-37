import copy

import logging
import pytest

from pytest_shell.connection import local_bash_connection
from pytest_shell.dialect import BashDialect, Dialect


class ShellSession(Dialect):
    """Encapsulates all the user-provided instruction about setting up the 
    test as well as providing the results of any commands run and helper 
    methods for checking various aspects.
    """

    def __init__(self, connection, envvars=None, source=None, pwd=None):
        self._initial_envvars = dict(envvars) if envvars else {}
        self._initial_source = list(source) if source else []
        self._initial_pwd = pwd
        self._depth = 0
        self.connection = connection
        self.auto_return_code_error = True
        self.last_return_code = 0

    def __call__(self, envvars=None, source=None, pwd=None):
        obj = copy.copy(self)
        obj._initial_envvars = dict(envvars) if envvars else {}
        obj._initial_source = list(source) if source else []
        obj._initial_pwd = pwd
        obj._depth = self._depth + 1
        return obj

    def __enter__(self):
        # This is pretty stupid, why would starting vs subshells be on different
        # objects?
        logger = logging.getLogger(__name__)
        if self._depth > 0:
            self.start_subshell()
        else:
            self.connection.start()
        if self._initial_pwd:
            self.cd(self._initial_pwd)
        logger.debug('Setting vars: %s', self._initial_envvars)
        for k, v in self._initial_envvars.items():
            self.set_env(k, v)
        for fname in self._initial_source:
            self.source(fname)
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        if self._depth == 0:
            self.connection.finish()
        else:
            self.exit()

    def send(self, command):
        out = self.connection.send(command)
        self.last_return_code = self.return_code()
        if self.last_return_code and self.auto_return_code_error:
            pytest.fail('Got non-zero return code %d when running "%s"' %
                        (self.last_return_code, command))
        return out

    def send_nowait(self, command):
        return self.connection.send_nowait(command)

    def wait_for(self, pattern_or_function, timeout=3.0):
        return self.connection.wait_for(pattern_or_function, timeout)


class LocalBashSession(ShellSession, BashDialect):

    def __init__(self, envvars=None, source=None, pwd=None, cmd='/bin/bash'):
        ShellSession.__init__(self, local_bash_connection(cmd=cmd),
                              envvars, source, pwd)


bash = LocalBashSession

