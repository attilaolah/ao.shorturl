import doctest
import unittest


docfiles = ('shorturl.rst', 'django.rst', 'appengine.rst')

docstrings = ('ao.shorturl',)


def test_suite():
    """Run all doctests in one test suite."""

    tests = [doctest.DocFileSuite(file,
        optionflags=doctest.ELLIPSIS) for file in docfiles]
    tests += [doctest.DocTestSuite(docstring,
        optionflags=doctest.ELLIPSIS) for docstring in docstrings]

    return unittest.TestSuite(tests)
