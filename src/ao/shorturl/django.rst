Using with Django and template tags
-----------------------------------

If you use Django, you can access an object's short URL from a template with
the ``shorturl`` template tag. To use it, add ``ao.shorturl`` to your
``INSTALLED_APPS``. Then in the template you can do something like this::

    {% load shorturl %}
    <a href="{% shorturl city %}">{{ city.name }}</a>

Note that this will create an *absolute* url.

Test the template tag::

    >>> from ao.shorturl.templatetags import shorturl

    >>> class Parser(object):
    ...     def split_contents(self):
    ...         return (None, 'xxx')
    ...

    >>> node = shorturl.shorturl(None, Parser())
    >>> node
    <ao.shorturl.templatetags.shorturl.URL object at ...>

    >>> node.render({'xxx': None})
    Traceback (most recent call last):
    ...
    NotImplementedError: You must overload `construct_url`.

Clean up after the tests::

    >>> from zope.testing import cleanup
    >>> cleanup.cleanUp()


