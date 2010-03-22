Using the short URL library with App Engine
===========================================

First set up a fake App Engine environment::

    >>> import minimock
    >>> import sys

    >>> mocks = (
    ...     'google',
    ...     'google.appengine',
    ...     'google.appengine.api',
    ...     'google.appengine.ext',
    ... )

    >>> sys.modules.update(dict((mock, minimock.Mock(mock)) for mock in mocks))

    >>> import ao.shorturl
    >>> import ao.shorturl.appengine
    Called google.appengine.ext.db.ReferenceProperty(...)

To use the App Engine backend, simply import it and pass it as the ``handler``
keyword argument to ``ao.shorturl.registerHandler()``::

    >>> handler = ao.shorturl.registerHandler(
    ...     handler=ao.shorturl.appengine.AppEngineShortUrlHandler,
    ... )

    >>> handler
    <ao.shorturl.appengine.AppEngineShortUrlHandler object at ...>

Cache context will use `google.appengine.api.memcache`::

    >>> context = minimock.Mock('context')
    >>> handler.cache_context('someurl', context)
    Called context.key()
    Called google.appengine.api.memcache.add('someurl', 'None', 1200)

1200 is the default value for the cache timeout, but you can overwrite it by
passing the ``url_cache_time`` parameter to ``ao.shorturl.registerHandler()``.

Test the cache return value::

    >>> from google.appengine.api import memcache
    >>> memcache.get.mock_returns = 'result'

    >>> handler.get_context_from_cache('someurl')
    Called google.appengine.api.memcache.get('someurl')
    Called google.appengine.ext.db.get('result')

On failure it raises a ``LookupError``::

    >>> memcache.get.mock_returns = None

    >>> handler.get_context_from_cache('someurl')
    Traceback (most recent call last):
    ...
    LookupError: Context key not found in the cache.

Same is true for the datastore storage backend. Let's fake the datastore to
return a context for any key::

    >>> class FakeMapping(object):
    ...     context = 'context'
    ...

    >>> ao.shorturl.appengine.ShortUrl.get_by_key_name.mock_returns = \
    ...     FakeMapping()
    >>> handler.get_context_from_db('someurl')
    Called ShortUrl.get_by_key_name('someurl')
    'context'

Otherwise it raises a ``LookupError``::

    >>> ao.shorturl.appengine.ShortUrl.get_by_key_name.mock_returns = None

    >>> handler.get_context_from_db('someurl')
    Traceback (most recent call last):
    ...
    LookupError: Context not found in the datastore.

Try to construct a URL::

    >>> class FakeQuery(list):
    ...     def count(self):
    ...         return 0
    ...

    >>> ao.shorturl.appengine.ShortUrl.mock_returns = minimock.Mock('shorturl')

    >>> context = minimock.Mock('context')
    >>> fakeurl = minimock.Mock('shorturl')
    >>> fakekey = minimock.Mock('shorturl.key')
    >>> fakekey.name.mock_returns = 'fooname'
    >>> fakeurl.key.mock_returns = fakekey
    >>> context.shorturl = FakeQuery((fakeurl,))

    >>> handler.construct_url(context)
    Called google.appengine.api.memcache.get('...')
    Called ShortUrl.get_by_key_name('...')
    Called ShortUrl(context=<Mock ... context>, key_name='...')
    Called shorturl.put()
    Called shorturl.key()
    Called shorturl.key.name()
    '/fooname'

Clean up after the tests::

    >>> from zope.testing import cleanup
    >>> cleanup.cleanUp()


