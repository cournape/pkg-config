A reimplementation of pkg-config in python.

Work in progress.

#### How to setup

To install it, simply clone this repository and do:

	$ pip install .

You can then use the package:

	$ python -m pkg_config --modversion libssl
	$ python -m pkg_config --cflags libssl
	$ python -m pkg_config --list-all

#### TODO

* support for every field
* support for PKG_CONFIG_PATH
* support for every `pkg-config` flag
