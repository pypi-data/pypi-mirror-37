===================================
The gocept.pytestlayer distribution
===================================

Integration of zope.testrunner-style test layers into the `py.test`_
framework

This package is compatible with Python versions 2.7 and 3.5 - 3.7 including
PyPy implementation. (To run its tests successfully you should use at least
Python 2.7.4 because of a bug in earlier Python 2.7 versions.)

.. _`py.test` : http://pytest.org

Quick start
===========

* Make sure your test files follow the `conventions of py.test's test
  discovery`_

  .. _`conventions of py.test's test discovery`:
     http://pytest.org/latest/goodpractises.html#python-test-discovery

  In particular, a file named ``tests.py`` will not be recognised.

* Add a buildout section to create the `py.test` runner::

    [buildout]
    parts += pytest

    [pytest]
    recipe = zc.recipe.egg
    eggs = gocept.pytestlayer
           pytest
           <YOUR PACKAGE HERE>

``gocept.pytestlayer`` registers itself as a ``py.test`` plugin. This way, nothing
more is needed to run an existing Zope or Plone test suite.

Advanced usage
==============

Version 2.1 reintroduced `fixture.create()` to be able to define the name of the generated to py.test fixtures. So it is possible to use them in function style tests.

Example (Code has to be in `contest.py`!)::

    from .testing import FUNCTIONAL_LAYER
    import gocept.pytestlayer.fixture

    globals().update(gocept.pytestlayer.fixture.create(
        FUNCTIONAL_LAYER,
        session_fixture_name='functional_session',
        class_fixture_name='functional_class',
        function_fixture_name='functional'))

This creates three fixtures with the given names and the scopes in the argument name. The session and class fixtures run `setUp()` and `tearDown()` of the layer if it has not been run before while the function fixture runs `testSetUp()` and `testTearDown()` of the layer. The function fixture depends on the session one. The fixtures return the instance of the layer. So you can use the `functional` fixture like this::

    def test_mymodule__my_function__1(functional):
        assert functional['app'] is not None

Not supported use cases
=======================

* Inheriting from a base class while changing the layer. See `issue #5`_

* Mixing classes inheriting ``unittest.TestCase`` and a ``test_suite()`` function (e. g. to create a ``DocTestSuite`` or a ``DocFileSuite``) in a single module (aka file).

  * This is a limitation of the `py.test` test discovery which ignores the doctests in this case.

  * Solution: Put the classes and ``test_suite()`` into different modules.

* A ``doctest.DocFileSuite`` which does not have a ``layer`` is silently skipped. Use the built-in doctest abilities of py.test to run those tests.

.. _`issue #5` : https://bitbucket.org/gocept/gocept.pytestlayer/issues/5


=============================
Developing gocept.pytestlayer
=============================

:Author:
    `gocept <http://gocept.com/>`_ <mail@gocept.com>,
    Godefroid Chapelle <gotcha@bubblenet.be>

:PyPI page:
    http://pypi.python.org/pypi/gocept.pytestlayer/

:Issues:
    https://bitbucket.org/gocept/gocept.pytestlayer/issues

:Source code:
    https://bitbucket.org/gocept/gocept.pytestlayer/

:Current change log:
    https://bitbucket.org/gocept/gocept.pytestlayer/raw/tip/CHANGES.rst


=================================
Change log for gocept.pytestlayer
=================================

6.0 (2018-10-24)
================

- Add support for Python 3.6, 3.7 and PyPy3.

- Drop support for Python 3.4.

- Fix tests to run with `pytest >= 3.9.1`.

- Release also as universal wheel.

- Update to new pytest fixture API to avoid DeprecationWarnings. (#10)


5.1 (2016-12-02)
================

- Make installation process compatible with `setuptools >= 30.0`.


5.0 (2016-08-23)
================

- Fix tests to pass if `pytest >= 3.0` is used for testing.


4.0 (2016-04-27)
================

- Support Python 3.4, 3.5 and PyPy.

- Use tox as testrunner.


3.0 (2016-04-14)
================

- Claim compatibility with py.test 2.9.x.

- Drop Python 2.6 support.

2.1 (2014-10-22)
================

- Update handling of keywords and doctest testnames for py.test-2.5.
  [wosc]

- Re-introduce ``gocept.pytestlayer.fixture.create()`` method, to allow giving
  created fixtures a non-random name, so other fixtures can depend on them.
  [tlotze, wosc]

- Generate session-scoped fixtures from layers in addition to class-scoped
  ones, if a session-scoped one is required somewhere, the class-scoped ones
  are simply ignored. [tlotze, wosc]


2.0 (2013-09-19)
================

- Remove need to explicitely create fixtures.
  [gotcha]

- Add ``plone.testing.layered`` test suites support.
  [gotcha]

- Made tests a bit more robust.
  [icemac]


1.0 (2013-08-28)
================

- Initial release.
  [tlotze, icemac, gotcha]


