import textwrap
import unittest

from pkg_config._models import PackageInfo


class TestPcFileHandling(unittest.TestCase):
    def test_ssl(self):
        # Given
        data = textwrap.dedent(u"""\
        prefix=/usr
        exec_prefix=${prefix}
        libdir=${exec_prefix}/lib
        includedir=${prefix}/include

        Name: OpenSSL
        Description: Secure Sockets Layer and cryptography libraries
        Version: 0.9.8zh
        Requires:
        Libs: -L${libdir} -lssl -lcrypto -lz
        Cflags: -I${includedir}
        """)

        # When
        pkg_info = PackageInfo.from_string(data)

        # Then
        self.assertEqual(pkg_info.name, u"OpenSSL")
        self.assertEqual(pkg_info.version, u"0.9.8zh")
        self.assertEqual(
            pkg_info.description, u"Secure Sockets Layer and cryptography libraries"
        )
        self.assertEqual(pkg_info.requires, u"")
        self.assertEqual(pkg_info.cflags, u"")
        self.assertEqual(pkg_info.libs, u"-lssl -lcrypto -lz")

        # When
        pkg_info = PackageInfo.from_string(data, pkg_config_compat=False)

        # Then
        self.assertEqual(pkg_info.cflags, u"-I/usr/include")
        self.assertEqual(pkg_info.libs, u"-L/usr/lib -lssl -lcrypto -lz")
