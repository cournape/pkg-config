from __future__ import print_function

import argparse
import sys

from pkg_config._commands import find_pc_file, list_all
from pkg_config._models import PackageInfo


VERSION = "0.0.1"

SEARCH_DIRECTORIES = [
    "/usr/local/lib/pkgconfig",
    "/usr/local/share/pkgconfig",
    "/usr/lib/pkgconfig",
    "/usr/local/Homebrew/Library/Homebrew/os/mac/pkgconfig/10.11",
]


def main(argv=None):
    argv = argv or sys.argv[1:]

    parser = argparse.ArgumentParser(
        description=u"pkg-config reimplementation in python.")

    parser.add_argument(
        u"--cflags", help=u"output all pre-processor and compiler flags",
        action="store_true"
    )
    parser.add_argument(
        u"--libs", help=u"output all linker flags", action="store_true"
    )
    parser.add_argument(
        u"--list-all", help=u"list all known packages", action="store_true"
    )
    parser.add_argument(u"--modversion", action="store_true")
    parser.add_argument(
        u"--print-requires-private", action="store_true",
    )
    parser.add_argument(
        u"--version", help=u"Print version and exits", action="store_true"
    )

    parser.add_argument(u"pc_file", nargs="?")

    namespace = parser.parse_args(argv)

    if namespace.version:
        print(VERSION)
        sys.exit(0)

    if namespace.list_all:
        list_all(SEARCH_DIRECTORIES)
        sys.exit(0)

    p = find_pc_file(SEARCH_DIRECTORIES, namespace.pc_file)
    pkg_info = PackageInfo.from_path(p)

    if namespace.cflags:
        print(pkg_info.cflags)
        sys.exit(0)

    if namespace.libs:
        print(pkg_info.libs)
        sys.exit(0)

    if namespace.modversion:
        print(pkg_info.version)
        sys.exit(0)

    if namespace.print_requires_private:
        print("\n".join(pkg_info.requires_private))
        sys.exit(0)


if __name__ == "__main__":
    main()
