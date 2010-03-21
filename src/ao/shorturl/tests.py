import doctest
import unittest


docfiles = ('shorturl.txt', 'django.txt')

docstrings = ('ao.shorturl',)

def test_suite():
    """Run all doctests in one test suite."""

    tests = [doctest.DocFileSuite(file,
        optionflags=doctest.ELLIPSIS) for file in docfiles]
    tests += [doctest.DocTestSuite(docstring,
        optionflags=doctest.ELLIPSIS) for docstring in docstrings]

    return unittest.TestSuite(tests)
