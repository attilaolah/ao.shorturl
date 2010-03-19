from ao.shorturl import getHandler

from django.template import Library, Node, Variable


handler = getHandler()
register = Library()


def shorturl(parser, token):
    """Return the short URL for the context."""

    context = token.split_contents()[1]

    return URL(context)

register.tag(shorturl)


class URL(Node):
    """The URL node."""

    def __init__(self, context):
        """Save the context variable to self.context."""

        self.context = Variable(context)

    def render(self, context):
        """Render the link for self.context."""

        return handler.construct_url(self.context.resolve(context))
