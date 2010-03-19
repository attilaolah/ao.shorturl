from zope.interface import Interface


class IShortUrl(Interface):
    """Interface for the global `ShortUrl` urility."""


class IShortUrlHandler(Interface):
    """Interface for ShortUrlHandler objects."""
