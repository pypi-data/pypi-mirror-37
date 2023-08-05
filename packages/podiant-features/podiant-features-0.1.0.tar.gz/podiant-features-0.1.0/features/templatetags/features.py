from django.template import Library, TemplateSyntaxError, Node, Variable
from .. import feature_enabled

register = Library()


@register.tag()
def feature(parser, token):
    try:
        tag_name, name = token.contents.split(None, 1)
    except ValueError:  # pragma: no cover
        raise TemplateSyntaxError(
            '%r tag requires a single argument' % token.contents.split()[0]
        )

    nodelist = parser.parse(('endfeature',))
    parser.delete_first_token()
    return FeatureNode(name, nodelist)


class FeatureNode(Node):
    def __init__(self, feature, nodelist):
        self.feature = feature
        self.nodelist = nodelist

    def render(self, context):
        feature = Variable(self.feature).resolve(context)
        request = context.get('request')

        if request is None:  # pragma: no cover
            return ''

        if feature_enabled(feature, request):
            return self.nodelist.render(context)

        return ''
