"""Packaging settings."""


from codecs import open
from os.path import abspath, dirname, join
from subprocess import call

from setuptools import Command, find_packages, setup

from repobot import __version__


this_dir = abspath(dirname(__file__))
with open(join(this_dir, 'README.rst'), encoding='utf-8') as file:
    long_description = file.read()


class RunTests(Command):
    """Run all tests."""
    description = 'run tests'
    user_options = []

    def initialize_options(self):
        pass

    def finalize_options(self):
        pass

    def run(self):
        """Run all tests!"""
        errno = call(['py.test', '--cov=skele', '--cov-report=term-missing'])
        raise SystemExit(errno)

setup(
    name = 'repobot',
    version = __version__,
    description = 'Programatic github repo automation',
    long_description = long_description,
    install_requires = ['requests', 'keyring>=15.1.0,<16', 'docopt'],
    python_requires = '>=3',
    url = 'https://github.com/nickpalenchar/repobot',
    author = 'Nick Palenchar',
    author_email = '',
    license = 'MIT',
    classifiers = ['Development Status :: 2 - Pre-Alpha',
            'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',],
    keywords = 'cli',
    packages = find_packages(exclude=['docs', 'tests*']), # prevents irrelevent files from being added to package
    extras_require = {
        'test': ['coverage', 'pytest', 'pytest-cov'],
    },
    entry_points = {
        'console_scripts': [
            'rbot=repobot.cli:main',
            'repobot=repobot.cli:main'
        ],
    },
    cmdclass = {'test': RunTests},
)
