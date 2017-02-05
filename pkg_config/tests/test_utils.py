import unittest

from pkg_config.utils import resolve_metadata, resolve_variables


class TestResolveVariables(unittest.TestCase):
    def test_no_substitution(self):
        # Given
        variables = {
            "prefix": "/usr",
            "libdir": "/usr/lib",
        }
        r_variables = variables.copy()

        # When
        resolved_variables = resolve_variables(variables)

        # Then
        self.assertEqual(resolved_variables, r_variables)

    def test_simple(self):
        # Given
        variables = {
            "prefix": "/usr",
            "libdir": "${prefix}/lib",
        }
        r_variables = {
            "prefix": "/usr",
            "libdir": "/usr/lib",
        }

        # When
        resolved_variables = resolve_variables(variables)

        # Then
        self.assertEqual(resolved_variables, r_variables)


class TestResolveMetadata(unittest.TestCase):
    def test_simple(self):
        # Given
        variables = {
            "prefix": "/usr",
            "includedir": "/usr/include",
            "libdir": "/usr/lib",
        }
        metadata = {
            "Cflags": "-I${includedir}",
            "Libs": "-L${libdir}",
        }
        r_metadata = {
            "Cflags": "-I/usr/include",
            "Libs": "-L/usr/lib",
        }

        # When
        resolved_metadata = resolve_metadata(metadata, variables)

        # Then
        self.assertEqual(resolved_metadata, r_metadata)
