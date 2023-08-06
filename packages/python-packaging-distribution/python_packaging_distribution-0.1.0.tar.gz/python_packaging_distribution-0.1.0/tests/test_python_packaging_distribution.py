#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Tests for `python_packaging_distribution` package."""


import unittest
from click.testing import CliRunner

from python_packaging_distribution import python_packaging_distribution
from python_packaging_distribution import cli


class TestPython_packaging_distribution(unittest.TestCase):
    """Tests for `python_packaging_distribution` package."""

    def setUp(self):
        """Set up test fixtures, if any."""

    def tearDown(self):
        """Tear down test fixtures, if any."""

    def test_000_something(self):
        """Test something."""

    def test_command_line_interface(self):
        """Test the CLI."""
        runner = CliRunner()
        result = runner.invoke(cli.main)
        assert result.exit_code == 0
        assert 'python_packaging_distribution.cli.main' in result.output
        help_result = runner.invoke(cli.main, ['--help'])
        assert help_result.exit_code == 0
        assert '--help  Show this message and exit.' in help_result.output
