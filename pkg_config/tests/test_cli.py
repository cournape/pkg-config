import mock
import unittest

from pkg_config.__main__ import VERSION, main


class TestCLI(unittest.TestCase):
    def test_version(self):
        # Given
        argv = ["--version"]

        # When
        with self.assertRaises(SystemExit):
            with mock.patch("pkg_config.__main__.print") as p:
                main(argv)

        # Then
        p.assert_called_with(VERSION)
