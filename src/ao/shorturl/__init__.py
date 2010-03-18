import random
import string


try:
    from ao.shorturl.interfaces import IShortUrlHandler
    from zope.component import queryUtility
except ImportError:
    # If zope.component and zope.interface are not available, that's still ok,
    # we will fall back to getting the configuration as a parameter.
    pass


class ShortUrlNotFound(LookupError):
    """Indicate that the shourt url being accessed is not found.

    Catch this error in a middleware or in the place where your framework
    handles exceptions and return a nice HTTP 404 page.

    """


class ShortUrl(object):
    """Base object for handling short URLs."""


    def __init__(self, handler=None, **config):
        """Initialize the object by setting loking up the handler."""

        try:
            self.handler = queryUtility(IShortUrlHandler)
        except NameError:
            self.handler = handler

        if self.handler is None:
            self.handler = ShortUrlHandler(config)  # fall back to the default


class ShortUrlHandler(object):
    """Default short URL handler.

    This class contains a set of defaults for the Short URL handler.

    """

    url_elems = string.digits + string.ascii_letters
    url_length = 6
    url_prefix = '/'

    def __init__(self, config={}):
        """Initialize using the given configuration."""

        for (k, v) in config.iteritems():
            setattr(self, k, v)

    def get_context(self, token):
        """Look up the context object for the token."""

        raise NotImplementedError('You must provide a `get_context` method.')

    def get_token(self, url):
        """Try to get a token for the given url.

        First tries to get the token from cache, then fall back to the database
        backend. If the token is not found by neither of the backends, raises
        `ao.shorturl.ShortUrlNotFound`.

        """

        try:
            token = self.get_token_from_cache(url)
        except LookupError:
            try:
                token = self.get_token_from_db(url)
            except LookupError:
                raise ShortUrlNotFound('Short URL could not be found: ' + url)

    def get_token_from_cache(self, url):
        """Overload this method to use memcached."""

        raise LookupError

    def get_token_from_db(self, url):
        """Overload this method to use the database/datastore."""

        raise LookupError

    def generate_url(self, len=None, elems=None):
        """Generate (a random) new url.

        Overload this method to customize the short URLs. The default behavior
        is to generate a random `length`-characters-long string using elements
        from `string.ascii_letters` + `string.digits`, check if there are any
        duplicates, and return a new, unique token.

        """

        len = len or self.url_length
        elems = elems or self.url_elems


        while True:
            url = ''.join(map(random.choice, (elems for x in xrange(len))))
            try:
                self.get_token(url)
                continue
            except LookupError:
                return url
