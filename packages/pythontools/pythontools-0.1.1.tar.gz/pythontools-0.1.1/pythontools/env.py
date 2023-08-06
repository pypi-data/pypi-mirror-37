"""
Environment handling
"""

import os
import platform
import subprocess
import sys
import tempfile
from contextlib import contextmanager


def _source_env_linux(env_file):
    """
    source_env implementation for Linux.
    """
    environ = {}
    output = subprocess.check_output(['bash', '-c', 'source %s && env --null' % env_file])
    output = output.decode('utf-8')
    variables = output.split('\x00')
    for var in variables:
        if var:
            key, _, value = var.partition("=")
            environ[key] = value
    return environ


def _source_env_darwin(env_file):
    """
    source_env implementation for MacOS.
    """
    environ = {}
    output = subprocess.check_output([
        'bash', '-c',
        'source %s && '
        '%s -c \'import os; '
        '[print("%%s=%%s" %% (key, value), end="\\0") '
        'for key, value in os.environ.items()]\'' % (env_file, sys.executable)
    ])
    output = output.decode('utf-8')
    variables = output.split('\x00')
    for var in variables:
        if var:
            key, _, value = var.partition("=")
            environ[key] = value
    return environ


def _source_env_windows(env_file):
    """
    source_env implementation for Windows.
    """
    environ = {}
    # Use a temp script to avoid quote issue with cmd
    script = tempfile.NamedTemporaryFile('w', suffix='.bat', delete=False)
    script.write('@echo off\n\n')
    script.write('call %s && '
                 '%s -c "import os; [print(\'%%%%s=%%%%s\' %%%% (key, value), end=\'\\0\') '
                 'for key, value in os.environ.items()]"' % (env_file, sys.executable))
    script.close()

    output = subprocess.check_output(['cmd', '/C', script.name])
    output = output.decode('utf-8')
    variables = output.split('\x00')
    for var in variables:
        if var:
            key, _, value = var.partition("=")
            environ[key] = value

    # Delete temp script
    os.remove(script.name)
    return environ


def source_env(env_file):
    """
    Reads the given file and create a new environment variable.
    This variable can be used to replace os.environ.

    :param env_file the path to the file to source.
    """
    if not os.path.exists(env_file):
        raise FileNotFoundError()

    if platform.system() == 'Darwin':
        return _source_env_darwin(env_file)
    if platform.system() == 'Windows':
        return _source_env_windows(env_file)
    return _source_env_linux(env_file)


@contextmanager
def set_env(environ):
    """
    Create a context with the given environment.

    :param environ a dict containing the envirnment variables.
    """
    old_env = dict(os.environ)
    try:
        for key, value in environ.items():
            os.environ[key] = value
        yield
    finally:
        os.environ.clear()
        os.environ.update(old_env)
