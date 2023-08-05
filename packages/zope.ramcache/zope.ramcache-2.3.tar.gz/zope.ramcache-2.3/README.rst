===================
 ``zope.ramcache``
===================


.. image:: https://img.shields.io/pypi/v/zope.ramcache.svg
        :target: https://pypi.python.org/pypi/zope.ramcache/
        :alt: Latest release

.. image:: https://img.shields.io/pypi/pyversions/zope.ramcache.svg
        :target: https://pypi.org/project/zope.ramcache/
        :alt: Supported Python versions

.. image:: https://travis-ci.org/zopefoundation/zope.ramcache.svg?branch=master
        :target: https://travis-ci.org/zopefoundation/zope.ramcache

.. image:: https://coveralls.io/repos/github/zopefoundation/zope.ramcache/badge.svg?branch=master
        :target: https://coveralls.io/github/zopefoundation/zope.ramcache?branch=master


This package provides a RAM-based cache implementation for Zope.

The class ``zope.ramcache.ram.RAMCache`` is a (persistent) object
meant to be shared between threads. It implements
``zope.ramcache.interfaces.ram.IRAMCache``, which provides a simple
interface to cache information as well as defines a maximum number and
age for cached entries.

The cache is based on the idea of using arbitrary objects as keys,
with the ability to associate additional information in the cache key
for any given object. For example, it's possible to cache information
for an object for multiple different users simultaneously.
