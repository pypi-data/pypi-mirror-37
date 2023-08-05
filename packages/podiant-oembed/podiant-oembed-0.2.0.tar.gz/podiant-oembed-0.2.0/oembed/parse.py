from .models import Resource
from . import settings, utils


def parse_html(value, ajax=False):
    if not value:
        return ''

    value = str(value)
    if '<p' not in value and '</p>' not in value:
        if not value.strip().startswith('<') and not value.strip().endswith('</p>'):
            value = '<p>%s</p>' % value

    match = settings.P_REGEX.search(value)
    while match is not None and match.end() <= len(value):
        start = match.start()
        end = match.end()
        groups = match.groups()

        url = groups[0]
        if not url.startswith('http:') and not url.startswith('https:'):
            match = settings.P_REGEX.search(value, start + len(url))
            continue

        inner = '<p><a href="%(url)s">%(url)s</a></p>' % {
            'url': url
        }

        if ajax:
            inner = utils.wrap_ajax(
                utils.make_printable(url),
                'unknown'
            )
        else:
            resource = Resource.load(url)
            inner = resource.to_html()

        value = value[:start] + inner + value[end:]
        match = settings.P_REGEX.search(value, start + len(inner))

    return value
