import os
import shutil
import tempfile

import pytest


def pytest_addoption(parser):
    parser.addoption(
        '--structmpd-leave', action='store_true', dest='structmpd-leave',
        help='not remove temporary directory')
    parser.addoption(
        '--structmpd-root', action='store', default=None,
        dest='structmpd-root',
        help='customize parent path of temporary directory')
    parser.addoption(
        '--structmpd-name', action='store', default=None,
        dest='structmpd-name',
        help='customize name of temporary directory')


@pytest.fixture(scope='session')
def tmpsessiondir(request):
    dir_name = request.config.getoption('structmpd-name')
    if dir_name is None:
        dir_name = request.session.name

    base = None
    root_path = request.config.getoption('structmpd-root')
    if root_path is None:
        base = tempfile.mkdtemp(prefix=dir_name + '_')
    else:
        base = os.path.join(os.path.abspath(root_path), dir_name)
        if not os.path.exists(base):
            os.makedirs(base)

    try:
        yield(base)
    finally:
        if not request.config.getoption('structmpd-leave'):
            shutil.rmtree(base)


def _make_new_directory(base):
    # when the function is run with parameterized test, the 'test_dir' has
    # already created, so create another directory with sequential ID
    seq_id = -1
    new_dir = base
    while os.path.exists(new_dir):
        seq_id += 1
        new_dir = '{}_{:d}'.format(base, seq_id)
    os.makedirs(new_dir)
    return new_dir


@pytest.fixture(scope='function')
def tmpfuncdir(request, tmpsessiondir):
    base = tmpsessiondir
    if request.cls is not None:
        cls_name = request.cls.__name__
        base = os.path.join(base, cls_name)
    func_name = request.function.__name__
    base = os.path.join(base, func_name)
    return _make_new_directory(base)
