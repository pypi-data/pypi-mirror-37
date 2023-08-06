=========
 Changes
=========

2.2.0 (2018-10-19)
==================

- Add support for Python 3.7.

- Drop support for ``setup.py test``.

2.1.0 (2017-07-25)
==================

- Add support for Python 3.5 and 3.6.

- Drop support for Python 2.6 and 3.3.


2.0.0 (2014-12-24)
==================

- Added support for PyPy.  (PyPy3 is pending release of a fix for:
  https://bitbucket.org/pypy/pypy/issue/1946)

- Add support for Python 3.4.

- Add support for testing on Travis.


2.0.0a1 (2013-02-25)
====================

- Add support for Python 3.3.

- Replace deprecated ``zope.interface.classProvides`` usage with equivalent
  ``zope.interface.provider`` decorator.

- Replace deprecated ``zope.interface.implements`` usage with equivalent
  ``zope.interface.implementer`` decorator.

- Drop support for Python 2.4 and 2.5.

- When loading this package's ZCML configuration, make sure to configure
  ``zope.component`` first since we require part of its configuration.


1.0.1 (2010-09-25)
==================

- Add undeclared but needed dependency on ``zope.component``.

- Add test extra to declare test dependency on ``zope.component[test]``.


1.0 (2009-05-19)
================

* Initial public release, derived from zope.app.component and
  zope.app.interface to replace them.
