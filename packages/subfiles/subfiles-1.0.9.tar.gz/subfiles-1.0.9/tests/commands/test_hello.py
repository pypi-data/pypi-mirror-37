"""Tests for our `subfiles hello` subcommand."""


from subprocess import PIPE, Popen as popen
from unittest import TestCase


class TestHello(TestCase):
    def test_returns_multiple_lines(self):
        output = popen(['ftypes', 'schema'], stdout=PIPE).communicate()[0]
        lines = str(output, 'utf-8').split('\n')
        self.assertTrue(len(lines) == 1)
