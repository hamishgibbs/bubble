import os
import pytest
from bubble.utils import language, scaffold


@pytest.fixture(scope="session")
def tmp_dir(tmpdir_factory):

    path = tmpdir_factory.mktemp("tmp")

    return str(path)


class TestLanguage():
    '''Test language extraction from file extansion'''

    def test_language_r(self):
        '''Test language extraction from R file'''

        path = 'file.R'

        assert language(path) == 'r'

    def test_language_py(self):
        '''Test language extraction from Python file'''

        path = 'file.py'

        assert language(path) == 'py'

    def test_language_abs(self):
        '''Test language extraction from absolute path file'''

        path = '/usr/anyone/file.R'

        assert language(path) == 'r'


def test_scaffold(tmp_dir):

    fn = tmp_dir + '/test_scaffold.py'

    scaffold(fn, 'test')

    assert os.path.exists(fn)


def test_scaffold_raises(tmp_dir):

    fn = tmp_dir + '/test_scaffold.py'

    with pytest.raises(Exception):
        scaffold(fn, b'test')
