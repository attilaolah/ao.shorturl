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


    def __init__(self, handler=None):
        """Initialize the object by setting loking up the handler."""

        try:
            self.handler = queryUtility(IShortUrlHandler)
        except NameError:
            self.handler = handler

        if self.handler is None:
            self.handler = ShortUrlHandler()  # fall back to the default

    def get_token(self, key):
        """Try to get a token for the given key.

        First tries to get the token from cache, then fall back to the database
        backend. If the token is not found by neither of the backends, raises
        `ao.shorturl.ShortUrlNotFound`.

        """

        try:
            token = self.handler.get_token_from_cache(key)
        except LookupError:
            try:
                token = self.handler.get_token_from_db(key)
            except LookupError:
                raise ShortUrlNotFound('The given url could not be found: ' + key)
