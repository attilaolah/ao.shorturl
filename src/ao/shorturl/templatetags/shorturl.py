import ao.shorturl

from django import template


register = template.Library()


def shorturl(parser, token):
    """Return the short URL for the context."""

    context = token.split_contents()[1]

    return URL(context)

register.tag(shorturl)


class URL(template.Node):
    """The URL node."""

    def __init__(self, context):
        """Save the context variable to self.context."""

        self.context = template.Variable(context)
        self.handler = ao.shorturl.getHandler()

    def render(self, context):
        """Render the link for self.context."""

        return self.handler.construct_url(self.context.resolve(context))
