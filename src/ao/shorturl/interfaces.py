import zope.interface as zi


class IShortUrlHandler(zi.Interface):
    """Interface for ShortUrlHandler objects."""

    url_cache_time = zi.Attribute(
        u'The maximum lifetime of a (url, key) pair in cache.',
    )
    url_elems = zi.Attribute(
        u'A sequence that is used when generating new URLs.',
    )
    url_length = zi.Attribute(
        u'The length of the generated URLs.',
    )
    url_prefix = zi.Attribute(
        u'The path that prefixes the URLs.',
    )


    def cache_context(url, context):
        """Cache the context (i.e. using memcache)."""

    def get_context_from_cache(url):
        """Look up the cached context."""

    def get_context_from_db(url):
        """Look up the context in the database."""

    def generate_url(len, elems):
        """Generate (a random) new url."""

    def assign_url(context):
        """Create a new URL for the context and assign it to the context."""

    def construct_url(context, request):
        """Construct the short url for the given context."""
