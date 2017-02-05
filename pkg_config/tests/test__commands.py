import mock
import os.path
import shutil
import tempfile
import unittest

from pkg_config._commands import list_all

LIBSSL = """
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
"""

LIBPCRE = """
# Package Information for pkg-config

prefix=/usr/local
exec_prefix=${prefix}
libdir=/usr/lib
includedir=${prefix}/include

Name: libpcre
Description: PCRE - Perl compatible regular expressions C library
Version: 8.02
Libs: -L${libdir} -lpcre
Cflags: -I${includedir} 
"""


class TestMain(unittest.TestCase):
    def setUp(self):
        self.tempdir = tempfile.mkdtemp()

    def tearDown(self):
        shutil.rmtree(self.tempdir)

    def write_pc_file(self, name, data):
        path = os.path.join(self.tempdir, name + ".pc")
        with open(path, "wt") as fp:
            fp.write(data)

    def test_list_all(self):
        # Given
        self.write_pc_file("libssl", LIBSSL)
        self.write_pc_file("libpcre", LIBPCRE)

        # When
        with mock.patch("pkg_config._commands.print") as p:
            list_all([self.tempdir])

        # Then
        self.assertEqual(p.call_count, 2)
        p.called_once_with(
            u"libssl  OpenSSL - Secure Sockets Layer and cryptography "
             "libraries"
        )
        p.called_once_with(
           u"libpcre libpcre - PCRE - Perl compatible regular "
            "expressions C library"
        )
