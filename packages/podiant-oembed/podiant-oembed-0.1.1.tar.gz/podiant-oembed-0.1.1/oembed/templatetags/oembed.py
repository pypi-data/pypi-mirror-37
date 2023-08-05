from django.template import Library
from ..parse import parse_html
register = Library()


@register.filter()
def oembed(value):
    return parse_html(value, ajax=True)
