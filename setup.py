from setuptools import setup

setup(
    name="pkg-config",
    version="0.0.1",
    packages=["pkg_config", "pkg_config.tests"],
    author="David Cournapeau",
    author_email="cournape@gmail.com",
    entry_points={
        "console_scripts": [
            "pkg-config-py = pkg_config.__main__:main",
        ],
    },
)
