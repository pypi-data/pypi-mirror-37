This package provides a calendar HTML export feature for `icemac.ab.calendar`_.

*Caution:* This package might not be as customizable as needed for a general
HTML calendar export.

.. _`icemac.ab.calendar` : https://pypi.org/project/icemac.ab.calendar

Copyright (c) 2015-2018 Michael Howitz

This package is licensed under the MIT License, see LICENSE.txt inside the
package.

.. contents::

=========
 Hacking
=========

Source code
===========

Get the source code::

   $ hg clone https://bitbucket.org/icemac/icemac.ab.calexport

or fork me on: https://bitbucket.org/icemac/icemac.ab.calexport

Running the tests
=================

To run the tests yourself call::

  $ virtualenv-2.7 .
  $ bin/pip install zc.buildout
  $ bin/buildout -n
  $ bin/py.test


===========
 Changelog
===========

1.9 (2018-10-13)
================

- Update to changes in test infrastructure in `icemac.addressbook >= 8.0`.

- Update to `icemac.ab.calendar >= 3.2`.

- Change installation procedure from `bootstrap.py` to `virtualenv`,
  see `README.txt`.


1.8 (2018-08-04)
================

- Add a missing migration for a refactoring in 1.7 possibly breaking export
  and master data.

- Update to changes in test infrastructure in `icemac.addressbook >= 7.0`.

- Change license from ZPL to MIT.

1.7 (2018-03-16)
================

- Update to `icemac.ab.calendar >= 3.0`.


Older versions
==============

See `OLD_CHANGES.rst`_.

.. _`OLD_CHANGES.rst` : https://bitbucket.org/icemac/icemac.ab.calexport/raw/default/OLD_CHANGES.rst


