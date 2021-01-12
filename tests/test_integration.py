import os
import pytest
from click.testing import CliRunner
from bubble import bubble


@pytest.fixture(scope="session")
def tmp_dir(tmpdir_factory):

    path = tmpdir_factory.mktemp("tmp")

    return str(path)


def test_init_project(tmp_dir):

    os.mkdir(tmp_dir + '/src')

    with open(tmp_dir + '/src/test.py', 'w') as f:

        f.write('# *** bubble make ***\nSome other stuff.\n# *** bubble input start ***\n"input1"\n"input2",\n"output"\n# *** bubble input end ***')

    runner = CliRunner()

    runner.invoke(bubble.init, ['--root', tmp_dir])

    assert os.path.exists(tmp_dir + '/bubble.json')


def test_create_makefile(tmp_dir):

    runner = CliRunner()

    runner.invoke(bubble.create, ['--file', tmp_dir + '/Makefile'])

    assert os.path.exists(tmp_dir + '/Makefile')


def test_create_python_template(tmp_dir):

    runner = CliRunner()

    runner.invoke(bubble.create, ['--file', tmp_dir + '/src/test.py'])

    assert os.path.exists(tmp_dir + '/src/test.py')


def test_make_targets(tmp_dir):

    assert os.path.exists(tmp_dir + '/bubble.json')
    assert os.path.exists(tmp_dir + '/Makefile')
    assert os.path.exists(tmp_dir + '/src/test.py')

    runner = CliRunner()

    runner.invoke(bubble.make, ['--root', tmp_dir])

    with open(tmp_dir + '/Makefile', 'r') as f:

        makefile_content = f.read()

    assert 'input1' in makefile_content
