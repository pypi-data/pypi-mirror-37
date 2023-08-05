#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Tests for `simple_jsondiff` package."""

import io
import json

import pytest

from click.testing import CliRunner

from simple_jsondiff import simple_jsondiff
from simple_jsondiff import cli


@pytest.fixture
def response():
    """Sample pytest fixture.

    See more at: http://doc.pytest.org/en/latest/fixture.html
    """
    # import requests
    # return requests.get('https://github.com/audreyr/cookiecutter-pypackage')


def test_content(response):
    """Sample pytest test function with the pytest fixture as an argument."""
    # from bs4 import BeautifulSoup
    # assert 'GitHub' in BeautifulSoup(response.content).title.string


def test_command_line_interface():
    """Test the CLI."""
    runner = CliRunner()
    with runner.isolated_filesystem():
        with open('first.json', 'w') as f:
            f.write("""
            {"a": 1}
            """)
        with open('second.json', 'w') as f:
            f.write("""
            {"a": 2}
            """)

        result = runner.invoke(cli.main, ["first.json", "second.json"])
        assert result.exit_code == 0
        assert '"a": 2' in result.output
        assert result.output == """{\n "a": 2\n}\n"""
        help_result = runner.invoke(cli.main, ['--help'])
        assert help_result.exit_code == 0
        assert '--help  Show this message and exit.' in help_result.output


def test_jsondiff():
    diff = simple_jsondiff.jsondiff("""
    {
        "a": 1,
        "b": 3
    }
    """, """
    {
        "a": 2,
        "b": 3,
        "c": 4
    }
    """)
    diff_dict = json.loads(diff)
    assert "a" in diff_dict, "value of 'a' changed so should be in diff"
    assert "b" not in diff_dict, "value of 'b' didn't change"
    assert "c" in diff_dict, "'c' was added"
    assert diff_dict["a"] == 2, "value of 'a' changed to 2"
