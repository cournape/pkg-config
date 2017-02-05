from __future__ import print_function

import glob
import os

from pkg_config._models import PackageInfo


def walk_directories(directories):
    for directory in directories:
        g = os.path.join(directory, "*.pc")
        for f in glob.glob(g):
            if os.path.isfile(f):
                yield os.path.join(g, f)


def parse_name_from_file(path):
    basename = os.path.basename(path)
    return os.path.splitext(basename)[0]


def list_all(directories):
    entries = []
    for p in walk_directories(directories):
        package_info = PackageInfo.from_path(p)
        name = parse_name_from_file(p)
        entries.append((name, package_info.name, package_info.description))

    m = max((name for name, _, _ in entries), key=len)
    fmt = u"{:%s}{} - {}" % (len(m) + 1,)

    for entry in entries:
        print(fmt.format(*entry))


def find_pc_file(directories, name):
    for p in walk_directories(directories):
        if parse_name_from_file(p) == name:
            return p

    raise RuntimeError(name)
