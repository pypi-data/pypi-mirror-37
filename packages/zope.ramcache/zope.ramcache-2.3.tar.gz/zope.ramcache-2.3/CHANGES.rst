=========
 Changes
=========

2.3 (2018-10-10)
================

- Add support for Python 3.7.


2.2.0 (2017-09-05)
==================

- Add support for Python 3.5 and 3.6.

- Drop support for Python 2.6 and 3.3.

- Drop support for ``python setup.py test``.

- Test PyPy3 on Travis CI.

- Stop requiring all values to support pickling in order to get
  statistics. Instead, return ``False`` for the size if such a value
  is found. Fixes `issue 1 <https://github.com/zopefoundation/zope.ramcache/issues/1>`_.

- Change the internal storage format of the RAM cache to require less
  memory and be easier to maintain.

2.1.0 (2014-12-29)
==================

- Added support for PyPy.  (PyPy3 is pending release of a fix for:
  https://bitbucket.org/pypy/pypy/issue/1946)

- Add support for Python 3.4.

- Add support for testing on Travis.


2.0.0 (2013-02-28)
==================

- Add support for Python 3.3.

- Replace deprecated ``zope.interface.implements`` usage with equivalent
  ``zope.interface.implementer`` decorator.

- Drop support for Python 2.4 and 2.5.

- Remove outdated classifier / keywords.

1.0 (2009-07-23)
================

- Broke out the ram cache functionality from ``zope.app.cache``.
