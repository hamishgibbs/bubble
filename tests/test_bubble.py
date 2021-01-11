import os
import pytest
from bubble.bubble import init
from click.testing import CliRunner


def test_init_bubble_project():

    runner = CliRunner()

    with runner.isolated_filesystem():

        result = runner.invoke(init)

    assert result.exit_code == 0
