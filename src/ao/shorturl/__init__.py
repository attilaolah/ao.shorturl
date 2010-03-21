import random
import string


try:
    from ao.shorturl.interfaces import IShortUrlHandler
    import zope.component as zc
    import zope.interface as zi
except ImportError:
    # If zope.component and zope.interface are not available, that's still ok,
    # we will fall back to getting the configuration as a parameter.

    IShortUrlHandler = None

    class zi(object):
        """Fallback for `zope.interface`."""

        def implements(self, *args, **kw):
            pass

    zi = zi()


handler = None


class ImproperlyConfigured(Exception):
    """Indicates that the short url handler is not configured properly."""


class ShortUrlNotFound(LookupError):
    """Indicate that the shourt url being accessed is not found.

    Catch this error in a middleware or in the place where your framework
    handles exceptions and return a nice HTTP 404 page.

    """


def getHandler(name=''):
    """Get the handler for the given name."""

    if name == '':
        global handler
    else:
        try:
            handler = zc.queryUtility(IShortUrlHandler, name=name)
        except NameError:
            raise ImproperlyConfigured('To use named handlers, you need to '\
                'make the `zope.component` package available.')

    if handler is None:
        raise ImproperlyConfigured('The requested handler is not initialized.')

    return handler


def registerHandler(handler=None, name='', **config):
    """Register a handler for the given name."""

    handler = (handler or BaseShortUrlHandler)(config)

    if name == '':
        globals()['handler'] = handler

    else:
        try:
            manager = zc.getSiteManager()
        except NameError:
            raise ImproperlyConfigured('To use named handlers, you need to '\
                'make the `zope.component` package available.')
        manager.registerUtility(handler, IShortUrlHandler, name=name)

    return handler


class BaseShortUrlHandler(object):
    """Default short URL handler.

    This class contains a set of defaults for the Short URL handler.

    * `url_cache_time` is the maximum lifetime of a (url, key) pair in cache.
    * `url_elems` is a sequence that is used when generating new URLs.
    * `url_length` is the length of the generated URLs.
    * `url_prefx` is the path that prefixes the URLs.

    Verify that the class implements the interface:

        >>> from zope.interface.verify import verifyClass
        >>> verifyClass(IShortUrlHandler, BaseShortUrlHandler)
        True

    Verify that the object provides the interface:

        >>> from zope.interface.verify import verifyObject
        >>> verifyObject(IShortUrlHandler, BaseShortUrlHandler())
        True

    """

    zi.implements(IShortUrlHandler)

    url_cache_time = 1200
    url_elems = string.digits + string.ascii_letters
    url_length = 6
    url_prefix = '/'
    url_pattern = lambda self, x: self.url_prefix + x

    def __init__(self, config={}):
        """Initialize using the given configuration."""

        for (k, v) in config.iteritems():
            setattr(self, k, v)

    def get_context(self, url):
        """Look up the context for the url.

        First try to get the context from cache, then, fall back to the
        database backend. If the context is not found by neither of the
        backends, raise `ao.shorturl.ShortUrlNotFound`.

        """

        try:
            context = self.get_context_from_cache(url)
        except LookupError:
            try:
                context = self.get_context_from_db(url)
            except LookupError:
                raise ShortUrlNotFound('Short URL could not be found: ' + url)

        self.cache_context(url, context)

        return context

    def cache_context(self, url, context):
        """Overload this method to cache the context (i.e. using memcache)."""

    def get_context_from_cache(self, url):
        """Overload this method to look up the cached context."""

        raise LookupError

    def get_context_from_db(self, url):
        """Overload this method to look up the context in the database."""

        raise LookupError

    def generate_url(self, len=None, elems=None):
        """Generate (a random) new url.

        Overload this method to customize the short URLs. The default behavior
        is to generate a random `length`-characters-long string using elements
        from `string.ascii_letters` + `string.digits`, check if there are any
        duplicates, and return a new, unique url.

        """

        len = len or self.url_length
        elems = elems or self.url_elems

        while True:
            url = ''.join((random.choice(elems) for x in xrange(len)))
            try:
                self.get_context(url)
                continue
            except LookupError:
                return url

    def assign_url(self, context):
        """Create a new URL for the context and assign it to the context."""

        raise NotImplementedError('You must overload `assign_url`.')

    def construct_url(self, context):
        """Construct the short url for the given context."""

        raise NotImplementedError('You must overload `construct_url`.')
