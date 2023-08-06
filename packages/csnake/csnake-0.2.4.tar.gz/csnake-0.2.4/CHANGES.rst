Changelog
================

0.2.0 (2018-10-08)
------------------

Features added
~~~~~~~~~~~~~~

* Complete rewrite of the original C-Snake


0.2.1 (2018-10-08)
------------------

Features added
~~~~~~~~~~~~~~

* Tested the CI pipeline for automatic PyPI upload


0.2.2 (2018-10-08)
------------------

Bug fixes
~~~~~~~~~

* Fixed erroneous documentation and PyPI info


0.2.3 (2018-10-08)
------------------

Bug fixes
~~~~~~~~~

* Fixed malformed RST on PyPI

0.2.4 (2018-10-29)
------------------

Features added
~~~~~~~~~~~~~~

* Added support for initialization of Values to PIL (pillow) Images through the
  `pil_image_to_list` utility in the optional `csnake.pil_converter` submodule.
* Enabled Pip package caching for CI
* Improved docstrings of some non-public functions
* Reformatted the Sphinx documentation somewhat.

Bug fixes
~~~~~~~~~

* Fixed several things in tests that produced warnings while testing.
* Fixed escape sequences in RST docstrings.

