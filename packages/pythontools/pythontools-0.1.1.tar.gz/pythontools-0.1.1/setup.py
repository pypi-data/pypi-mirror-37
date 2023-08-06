"""A setuptools based setup module.
See:
https://packaging.python.org/en/latest/distributing.html
https://github.com/pypa/sampleproject
"""

import os
import re

# Always prefer setuptools over distutils
from setuptools import setup, find_packages


def get_requires(filename):
    """
    List all the requirements from the given file.
    """
    requirements = []
    if not os.path.exists(filename):
        return requirements
    with open(filename, "rt") as req_file:
        for line in req_file.read().splitlines():
            if not line.strip().startswith("#"):
                requirements.append(line)
    return requirements

PROJECT_REQUIREMENTS = get_requires("requirements.txt")
DEV_REQUIREMENTS = get_requires("requirements_dev.txt")

def load_description():
    """
    Read the contents of your README file
    """
    this_directory = os.path.abspath(os.path.dirname(__file__))
    with open(os.path.join(this_directory, 'README.md'), encoding='utf-8') as f:
        long_description = f.read()
    return long_description

def load_version():
    """
    Loads the version from a file.
    """
    filename = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                            'pythontools', '__init__.py')
    with open(filename, 'rt') as version_file:
        pythontools_init = version_file.read()
        version = re.search("__version__ = '([0-9a-z.-]+)'", pythontools_init).group(1)
        return version

setup(
    name='pythontools',
    # Versions should comply with PEP440.  For a discussion on single-sourcing
    # the version across setup.py and the project code, see
    # https://packaging.python.org/en/latest/single_source_version.html
    version=load_version(), # + ".rc1",

    description='Python Tools provides several utility functions and tools that can be used in Python projects.',
    long_description=load_description(),
    long_description_content_type='text/markdown',

    # The project's main homepage.
    url='https://gitlab.com/osechet/pythontools',

    # Author details
    author='Olivier Sechet',
    author_email='osechet@gmail.com',

    # Choose your license
    license='MIT',

    # See https://pypi.python.org/pypi?%3Aaction=list_classifiers
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Build Tools',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3 :: Only',
    ],

    # What does your project relate to?
    keywords=['developer', 'tool', 'utility'],

    # You can just specify the packages manually here if your project is
    # simple. Or you can use find_packages().
    packages=find_packages(exclude=["tests"]),

    # List run-time dependencies here.  These will be installed by pip when
    # your project is installed. For an analysis of "install_requires" vs pip's
    # requirements files see:
    # https://packaging.python.org/en/latest/requirements.html
    install_requires=PROJECT_REQUIREMENTS,

    # List additional groups of dependencies here (e.g. development
    # dependencies). You can install these using the following syntax,
    # for example:
    # $ pip install -e .[dev,test]
    extras_require={
        'dev': DEV_REQUIREMENTS,
        'test': DEV_REQUIREMENTS,
    },

    # If there are data files included in your packages that need to be
    # installed, specify them here.  If using Python 2.6 or less, then these
    # have to be included in MANIFEST.in as well.
    package_data={
        'pythontools': ['*.txt'],
    },

    # Although 'package_data' is the preferred approach, in some case you may
    # need to place data files outside of your packages. See:
    # http://docs.python.org/3.4/distutils/setupscript.html#installing-additional-files # noqa
    # In this case, 'data_file' will be installed into '<sys.prefix>/my_data'
    # data_files=[('my_data', ['data/data_file'])],

    # To provide executable scripts, use entry points in preference to the
    # "scripts" keyword. Entry points provide cross-platform support and allow
    # pip to create the appropriate form of executable for the target platform.
    entry_points={
    },
)
