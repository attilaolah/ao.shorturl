from ao.shorturl import ShortUrlHandler

from google.appengine.api import memcache
from google.appengine.ext import db


class ShortUrl(db.Model):
    """Stores the short URL tokens in the datastore."""

    context = db.ReferenceProperty(collection_name='shorturl')


class ShortUrlHandler(ShortUrlHandler):
    """Short URL handler for Google App Engine.

    Uses the Datastore to store URLs and tokens, and the Memcache API for
    caching tokens.

    """

    def cache_context(self, url, context):
        """Store the context's key name and kind in memcache."""

        memcache.add(url, str(context.key()), self.url_cache_time)

    def get_context_from_cache(self, url):
        """Get the token from memcache."""

        key = memcache.get(url)
        if key is None:
            raise LookupError

        return db.get(key)

    def get_context_from_db(self, url):
        """Get the context from the datastore."""

        mapping = ShortUrl.get_by_key_name(url)
        if mapping is None:
            raise LookupError

        return mapping.context

    def assign_url(self, context):
        """Create a new URL for the context and assign it to the context."""

        url = ShortUrl(key_name=self.generate_url(), context=context)
        url.put()
