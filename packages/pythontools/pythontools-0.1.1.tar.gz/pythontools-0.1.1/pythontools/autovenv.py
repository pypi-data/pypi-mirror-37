"""
Provides functions to manage auto activation of virtualenv.
"""

import logging
import os
import platform
import subprocess
import sys
import venv
from distutils.sysconfig import get_python_lib

from . import env


# The name of the directory storing the virtual env
DEFAULT_VENV_DIR = 'venv'


def logger():
    """
    Returns the module's logger.
    """
    return logging.getLogger(__name__)


class Project:
    """
    The Project class represents a project associated with a virtual env. The project is
    identified with its path; the virtual env with its name.
    The Project class provides several methods useful to manipulate the virtual env.
    """

    def __init__(self, project_path, venv_dir=DEFAULT_VENV_DIR):
        self.project_path = project_path
        self.venv_dir = venv_dir
        self.venv_path = os.path.join(project_path, venv_dir)


    def has_venv(self):
        """
        Returns True if venv is setup for the project.
        """
        if os.path.exists(self.venv_path):
            return os.path.exists(os.path.join(self.venv_path, 'bin', 'python')) \
                or os.path.exists(os.path.join(self.venv_path, 'Scripts', 'python.exe'))
        return False


    def create_venv(self):
        """
        Creates the virtualenv.
        """
        logger().debug("Creating virtualenv into %s", self.venv_path)
        venv.create(self.venv_path, with_pip=True)


    def is_venv_activated(self):
        """
        Returns True if the virtual environment is activated.
        """
        python_lib = get_python_lib()
        return python_lib.startswith(os.path.join(self.venv_path))


    def activate_venv(self):
        """
        Activates the virtualenv.
        """
        if not self.has_venv():
            self.create_venv()

        logger().debug("Activating '%s' virtualenv", self.venv_dir)
        if platform.system() != "Windows":
            bin_dir = os.path.join(self.venv_path, 'bin')
            activate_name = 'activate'
            python_name = 'python'
        else:
            bin_dir = os.path.join(self.venv_path, 'Scripts')
            activate_name = 'activate.bat'
            python_name = 'python.exe'
        environ = env.source_env(os.path.join(bin_dir, activate_name))
        with env.set_env(environ):
            # Restart the script inside new environment
            logger().debug("Restarting python from virtual env...")
            proc = subprocess.Popen([os.path.join(bin_dir, python_name)] + sys.argv)
            proc.wait()
            logger().debug("Stopping initial python process...")
            exit(proc.returncode)


    def setup_venv(self, requirements=None):
        """
        Setups the virtualenv.

        :param requirements a list of requirements files.
        :raise FileNotFoundError if the venv is not created.
        """
        self.ensure_venv()

        logger().debug("Setting up '%s' virtualenv", self.venv_dir)
        # Update pip
        subprocess.check_output([
            'python', '-m',
            'pip', 'install', '--upgrade', 'pip',
        ])
        if not requirements:
            return
        for requirement in requirements:
            requirement_path = os.path.join(self.project_path, requirement)
            if not os.path.exists(requirement_path):
                logger().debug("Requirements file %s does not exist. Ignored.", requirement)
            else:
                logger().debug("Installing requirements from %s...", requirement)
                subprocess.check_output([
                    'python', '-m',
                    'pip', 'install', '-r', requirement_path,
                ])


    def ensure_venv(self):
        """
        Ensure the given venv exists and is activated, creating it and activating it if needed.
        """
        if not self.has_venv():
            logger().debug("Virtual env does not exist. Creating it...")
            self.create_venv()

        if not self.is_venv_activated():
            logger().debug("Virtual env is not activated. Activating it...")
            self.activate_venv()


def ensure_venv(project_path, venv_dir):
    """
    Ensure the given venv exists and is activated, creating it and activating it if needed.
    """
    project = Project(project_path, venv_dir)
    project.ensure_venv()
    return project.venv_path


def setup_venv(project_path, venv_dir, requirements):
    """
    Setups the virtualenv.

    :param requirements a list of requirements files. i.e.
           ['requirements.txt', 'requirements-dev.txt']
    """
    project = Project(project_path, venv_dir)
    project.setup_venv(requirements)
