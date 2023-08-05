"""
    pytest config for sphinxcontrib/imageembed/tests
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    :copyright: Copyright 2018 by Jan Gutter <github@jangutter.com>
    :license: BSD, see LICENSE for details.
"""

import os
import shutil
import sys

import pytest
from sphinx.testing.path import path

pytest_plugins = 'sphinx.testing.fixtures'

# Exclude 'roots' dirs for pytest test collector
collect_ignore = ['roots']


@pytest.fixture(scope='session')
def rootdir():
    return path(os.path.dirname(__file__) or '.').abspath() / 'roots'


def pytest_report_header(config):
    return 'Running Sphinx test suite (with Python %s)...' % (
        sys.version.split()[0])


def _initialize_test_directory(session):
    testroot = os.path.join(str(session.config.rootdir), 'tests')
    tempdir = os.path.abspath(
        os.getenv('SPHINX_TEST_TEMPDIR', os.path.join(testroot, 'build')))
    os.environ['SPHINX_TEST_TEMPDIR'] = tempdir

    print('Temporary files will be placed in %s.' % tempdir)

    if os.path.exists(tempdir):
        shutil.rmtree(tempdir)

    os.makedirs(tempdir)


def pytest_sessionstart(session):
    _initialize_test_directory(session)
