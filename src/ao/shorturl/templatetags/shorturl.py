from django.template import Library


register = Library()


def shorturl(parser, token):
    """Return the short URL for the context."""

    obj = token.split_contents()[1]

    return handler.build_url(obj)
