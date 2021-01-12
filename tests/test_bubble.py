import os
import pytest
from bubble.bubble import init
from click.testing import CliRunner


@pytest.fixture(scope="session")
def tmp_dir(tmpdir_factory):

    path = tmpdir_factory.mktemp("tmp")

    return str(path)


def test_init_bubble_project(tmp_dir):

    runner = CliRunner()

    runner.invoke(init, ['--root', tmp_dir])

    assert os.path.exists(tmp_dir + '/bubble.json')
