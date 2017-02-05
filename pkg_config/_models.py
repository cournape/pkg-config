import re

from pkg_config.utils import resolve_metadata, resolve_variables


R_COMMENT = re.compile("^\s*#")
R_VAR = re.compile("^([^=]+)=\s*(.*)$")
R_METADATA = re.compile("^([^:]+):\s*(.*)$")

R_REPLACE = re.compile("\$\{([^\}])+\}")

_NAME = "Name"
_DESCRIPTION = "Description"
_VERSION = "Version"
_CFLAGS = "Cflags"
_LIBS = "Libs"
_REQUIRES = "Requires"
_REQUIRES_PRIVATE = "Requires.private"


def _parser(data):
    variables = {}
    metadata = {}

    for line in data.splitlines():
        m = R_COMMENT.match(line)
        if m:
            continue
        m = R_VAR.match(line)
        if m:
            variables[m.group(1)] = m.group(2)
            continue
        m = R_METADATA.match(line)
        if m:
            name = m.group(1)
            value = m.group(2)
            metadata[name] = value
            continue

    variables = resolve_variables(variables)
    metadata = resolve_metadata(metadata, variables)
    return variables, metadata


class PackageInfo(object):
    @classmethod
    def from_path(cls, filename, pkg_config_compat=True):
        with open(filename, "rt") as fp:
            data = fp.read()

        return cls.from_string(data, pkg_config_compat)

    @classmethod
    def from_string(cls, s, pkg_config_compat=True):
        variables, metadata = _parser(s)

        requires = metadata.get(_REQUIRES, "")
        requires_private = metadata.get(_REQUIRES_PRIVATE, "")

        cflags = metadata.get(_CFLAGS, "")
        libs = metadata.get(_LIBS, "")

        if pkg_config_compat:
            cflags = " ".join(
                k for k in cflags.split() if k != "-I/usr/include"
            )
            libs = " ".join(
                k for k in libs.split() if k != "-L/usr/lib"
            )

        return cls(
            metadata[_NAME], metadata[_DESCRIPTION], metadata[_VERSION],
            requires, requires_private, cflags, libs,
        )

    def __init__(self, name, description, version, requires=u"",
                 requires_private=u"", cflags=u"", libs=u""):
        self.name = name
        self.description = description
        self.version = version

        self.requires = requires
        self.requires_private = requires_private

        self.cflags = cflags
        self.libs = libs
