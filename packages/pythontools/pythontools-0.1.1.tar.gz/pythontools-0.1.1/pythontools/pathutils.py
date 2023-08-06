"""
Path handling functions.
"""

import logging
import os
from contextlib import contextmanager


def logger():
    """
    Returns the module's logger.
    """
    return logging.getLogger(__name__)


@contextmanager
def chdir(dir_path):
    """
    Change working directory for the context.
    """
    old_dir = os.getcwd()
    try:
        if dir_path != old_dir:
            os.chdir(dir_path)
            logger().debug("Now in %s", os.getcwd())
        yield
    finally:
        if dir_path != old_dir:
            os.chdir(old_dir)
            logger().debug("Now in %s", os.getcwd())
