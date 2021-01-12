import os
from pathlib import Path
import pytest
from bubble import makefile


@pytest.fixture(scope="session")
def tmp_dir(tmpdir_factory):

    path = tmpdir_factory.mktemp("tmp")

    return str(path)


def test_should_be_made_true(tmp_dir):

    fn = tmp_dir + '/make_test_true.py'

    with open(fn, 'w') as f:

        f.write('# *** bubble make ***\nSome other stuff.')

    res = makefile.should_be_made(fn)

    assert res


def test_should_be_made_false(tmp_dir):

    fn = tmp_dir + '/make_test_false.py'

    with open(fn, 'w') as f:

        f.write('Some other stuff.')

    res = makefile.should_be_made(fn)

    assert not res


def test_find_py_files(tmp_dir):

    test_fn = 'test.py'

    Path(tmp_dir + '/' + test_fn).touch()

    res = makefile.find_files(tmp_dir, '.py')

    assert os.path.exists(tmp_dir + '/' + test_fn)
    assert type(res[0]) is str


def test_find_files_to_be_made(tmp_dir):

    res = makefile.find_files_to_be_made(tmp_dir, '.py')

    assert len(res) == 1

    assert type(res[0]) == str


def test_get_bubble_template_dependencies(tmp_dir):

    fn = tmp_dir + '/make_test_input.py'

    file_content = '# *** bubble input start ***\n"input1",\n"input2",\n"output"\n# *** bubble input end ***'

    with open(fn, 'w') as f:

        f.write(file_content)

    res = makefile.get_bubble_template_dependencies(fn)

    assert type(res) is list

    assert len(res) == 3
