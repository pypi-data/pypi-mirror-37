"""
This script can be used to simplify the initialization of a repository after the clone and pull
operations. It creates and setups a virtual environment if necessary and initializes the git
submodules.
To use this script in your project, copy it and it's project-tools dependency to a
script/projecttools directory. In the root directory of your project, create a init.py script as
follow:

>>> #!/usr/bin/env python3
>>>
>>> from script.pythontools import init
>>>
>>> if __name__ == '__main__':
>>>     init.run(os.path.dirname(os.path.realpath(__file__)), 'venv')
"""

import argparse
import logging
import os
import platform
import subprocess

from .ansicolors import color
from . import autovenv
from . import loggerutils
from . import pathutils


def logger():
    """
    Returns the module's logger.
    """
    return logging.getLogger(__name__)


def _init_logging():
    """
    Init the logs.
    """
    root_logger = logging.getLogger('')
    root_logger.setLevel(logging.DEBUG)
    console = logging.StreamHandler()
    console.setLevel(logging.INFO)
    formatter = loggerutils.ColoredFormatter()
    console.setFormatter(formatter)
    root_logger.addHandler(console)
    return console


def init_git_submodules(project_path):
    """
    Init git submodules
    """
    if not os.path.exists(os.path.join(project_path, '.gitmodules')):
        return

    logger().debug("Updating submodules...")
    with pathutils.chdir(project_path):
        subprocess.check_output(['git', 'submodule', 'update', '--init'])


def activate_command(venv_dir):
    """
    Returns the command used to activate the virtual env.
    """
    if platform.system() == 'Windows':
        return '.\\%s\\Scripts\\activate.bat' % venv_dir
    return '. ./%s/bin/activate' % venv_dir


def run(project_path, venv_name):
    """
    The main function.
    """
    # Initialize default logger
    handler = _init_logging()

    parser = argparse.ArgumentParser()
    parser.add_argument('-d', '--debug', action='store_true',
                        help='Print debug logs')

    args = parser.parse_args()

    if args.debug:
        handler.setLevel(logging.DEBUG)

    logger().info("Preparing virtual env...")
    autovenv.ensure_venv(project_path, venv_name)
    logger().info("Initializing git submodules...")
    init_git_submodules(project_path)
    logger().info("Setting up virtual env...")
    autovenv.setup_venv(project_path, venv_name,
                        requirements=['requirements.txt', 'requirements-dev.txt'])

    logger().info(color("Operation completed.", style='bold'))
    logger().info("You can enable the virtual env with:\n%s",
                  color(activate_command(venv_name), style='bold'))
