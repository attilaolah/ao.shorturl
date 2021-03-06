Using the short URL library without any framework
=================================================


Registering and getting handlers
--------------------------------

To use the library, you need to register a *handler* first, using the
``ao.shorturl.registerHandler()`` function. To get back the handler, use the
``getHandler()`` function::

    >>> from ao import shorturl
    >>> shorturl.getHandler()
    Traceback (most recent call last):
    ...
    ImproperlyConfigured: The requested handler is not initialized.

    >>> handler = shorturl.registerHandler()
    >>> shorturl.getHandler() is handler
    True
    >>> handler
    <ao.shorturl.BaseShortUrlHandler object at ...>

Note that if you intend to use multiple handlers, you need to give them
*names*, as the default handler is stored as a module global. However, to
utilize named handlers, you need to make the ``zope.component`` and
``zope.interface`` packages available. Each handler is stored in the local
site, meaning that if you use multiple sites, you can have different handlers
with the same name on a per-site basis. However, the unnamed handler is still
a *module* *global*, so take thet in consideration when using multiple
handlers and sites::

    >>> foo = shorturl.registerHandler(name='foo')
    >>> shorturl.getHandler(name='foo') is shorturl.getHandler('foo') is foo
    True

If you don't have the ``zope.component`` and ``zope.interface`` packages
available, you won't be able to use named handlers.

Let's pretend we don't have ``zope.component`` and ``zope.interface``::

    >>> import sys

    >>> class _():
    ...     def __init__(self, modules):
    ...         self.modules = modules
    ...
    ...     def find_module(self, fullname, path=None):
    ...         if fullname in self.modules:
    ...             raise ImportError('Debug import failure for %s' % fullname)
    ...

    >>> fail_loader = _(['zope.component', 'zope.interface'])
    >>> sys.meta_path.append(fail_loader)

    >>> for elem in ('zope.component', 'zope.interface'):
    ...     del sys.modules[elem]
    ...

    >>> reload(shorturl)
    <module 'ao.shorturl' from '...'>

    >>> del shorturl.zc  # delete the leftover zope.component module

    >>> shorturl.registerHandler(name='bar')
    Traceback (most recent call last):
    ...
    ImproperlyConfigured: To use named handlers, you need to make the ...

    >>> shorturl.getHandler('bar')
    Traceback (most recent call last):
    ...
    ImproperlyConfigured: To use named handlers, you need to make the ...

Remove our import hook::

    >>> del sys.meta_path[0]


Configuring the handler
-----------------------

To overwrite any default handler configuration, just pass the apropriate
keyword argument to the ``ao.shorturl.registerHandler()`` function::

    >>> len(shorturl.registerHandler().generate_url())
    6

    >>> len(shorturl.registerHandler(url_length=10).generate_url())
    10

    >>> shorturl.registerHandler(url_length=10, url_elems='x').generate_url()
    'xxxxxxxxxx'


Using custom handlers
---------------------

When calling ``ao.shorturl.registerHandler()`` without a ``handler`` argument,
it will not have any real functionality::

    >>> shorturl.registerHandler().assign_url(None)
    Traceback (most recent call last):
    ...
    NotImplementedError: You must overload `assign_url`.

    >>> shorturl.registerHandler().construct_url(None)
    Traceback (most recent call last):
    ...
    NotImplementedError: You must overload `construct_url`.

Registering a custom handler is easy, just subclass
``ao.shorturl.BaseShortUrlHandler``::

    >>> class FancyShortUrlHandler(shorturl.BaseShortUrlHandler):
    ...     def assign_url(self, context):
    ...         context['shorturl'] = self.generate_url()
    ...     def get_context_from_cache(self, url):
    ...         if context['shorturl'] == url:
    ...             return context
    ...         raise LookupError
    ...
    >>> handler = shorturl.registerHandler(handler=FancyShortUrlHandler, url_length=20)
    >>> handler
    <FancyShortUrlHandler object at ...>

    >>> context = {'foo': 'bar'}
    >>> handler.assign_url(context)
    >>> len(context['shorturl']) == 20
    True

As for now, there's one custom handler provided for App Engine:
``ao.shorturl.appengine.AppEngineShortUrlHandler``. It uses the datastore API
to store the short url associations and the memcache API to cache the keys for
better performance.


Getting the context from the handler
------------------------------------

In your view (if you're using an MCV framework), you can call the handler's
``get_context()`` method to query the context for a given short url::

    >>> handler.get_context('xxx')
    Traceback (most recent call last):
    ...
    ShortUrlNotFound: Short URL could not be found: xxx

    >>> handler.get_context(context['shorturl']) is context
    True

Note that ``ao.shorturl.get_context()`` will be called at least once each time a
new short url is created, to check for duplicates::

    >>> fired = False
    >>> def get_context(name):
    ...     global fired
    ...     if not fired:
    ...         print 'This URL already exists!'
    ...         fired = True
    ...         return 'Dummy context'
    ...     raise LookupError
    ...

    >>> handler.get_context = get_context

    >>> handler.generate_url()
    This URL already exists!
    '...'

Clean up after the tests::

    >>> from zope.testing import cleanup
    >>> cleanup.cleanUp()


