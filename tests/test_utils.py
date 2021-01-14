import os
import pytest
from bubble import utils


@pytest.fixture(scope="session")
def tmp_dir(tmpdir_factory):

    path = tmpdir_factory.mktemp("tmp")

    return str(path)


def test_language_r():
    '''Test language extraction from R file'''

    path = 'file.R'

    assert utils.language(path) == 'r'


def test_language_py():
    '''Test language extraction from Python file'''

    path = 'file.py'

    assert utils.language(path) == 'py'


def test_language_makefile():
    '''Test language extraction from Python file'''

    path = 'Makefile'

    assert utils.language(path) == 'makefile'


def test_language_raises():
    '''Test language extraction from Python file'''

    path = 'file.xml'

    with pytest.raises(ValueError):
        utils.language(path)


def test_language_abs():
    '''Test language extraction from absolute path file'''

    path = '/usr/anyone/file.R'

    assert utils.language(path) == 'r'


def test_scaffold(tmp_dir):

    fn = tmp_dir + '/test_scaffold.py'

    utils.scaffold(fn, 'test', True)

    assert os.path.exists(fn)


def test_scaffold_raises(tmp_dir):

    fn = tmp_dir + '/src/test_scaffold.py'

    with pytest.raises(Exception):

        utils.scaffold(fn, 'test')


def test_scaffold_tag(tmp_dir):

    fn = tmp_dir + '/test_scaffold.py'

    os.remove(fn)

    utils.scaffold(fn, 'test', False)

    with open(fn, 'r') as f:

        content = f.read()

    assert 'Template by bubble with <3' in content


def test_get_bubble_config(tmp_dir):

    utils.write_bubble_config(tmp_dir)

    res = utils.get_bubble_config(tmp_dir)

    assert type(res) is dict


def test_get_bubble_config_raises(tmp_dir):

    os.remove(tmp_dir + '/bubble.json')

    with pytest.raises(FileNotFoundError):
        utils.get_bubble_config(tmp_dir)
