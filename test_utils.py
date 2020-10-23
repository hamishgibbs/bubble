import os
import shutil
import pytest
import utils
from os import path


@pytest.fixture
def short_fn():

    return('file.R')


@pytest.fixture
def long_fn():

    return('/usr/bubble/tmp/file.R')


@pytest.fixture
def unsupported_fn():

    return('file.js')


def try_tmp():

    p = os.getcwd() + '/tmp'

    if path.exists(p):

        shutil.rmtree(p)

    try:

        os.mkdir(p)

    except Exception as e:

        shutil.rmtree(p)

        pass


class TestParseFn():

    def test_parse_fn_language(self, short_fn):
        '''Function to test language parsing'''

        res = utils.parse_fn(short_fn)

        assert res['language'] == 'R'

    def test_parse_fn_fn(self, short_fn):
        '''Function to test filename parsing'''

        res = utils.parse_fn(short_fn)

        assert res['fn'] == 'file.R'

    def test_parse_fn_path(self, long_fn):
        '''Function to test filepath parsing'''

        res = utils.parse_fn(long_fn)

        assert res['path'] == '/usr/bubble/tmp'

    def test_parse_fn_errors(self, unsupported_fn):
        '''Function to test errors are raised for unsupported file types'''

        with pytest.raises(ValueError):

            utils.parse_fn(unsupported_fn)


class TestWriteTemplate():

    def test_write_template_relative(self, short_fn):
        '''Test that files are being written to the correct directory given
            a relative path'''

        fn = utils.parse_fn('tmp/' + short_fn)

        try_tmp()

        utils.write_template(b'anything', fn)

        try:

            assert path.exists('tmp/file.R')

            shutil.rmtree(os.getcwd() + '/tmp')

        except:

            shutil.rmtree(os.getcwd() + '/tmp')

    def test_write_template_absolute(self, long_fn):
        '''Test that files are being written to the correct directory given
            an absolute path'''

        fn = utils.parse_fn(long_fn)

        try_tmp()

        utils.write_template(b'anything', fn)

        try:

            assert path.exists('tmp/file.R')

            shutil.rmtree(os.getcwd() + '/tmp')

        except:

            shutil.rmtree(os.getcwd() + '/tmp')
