from django.template.loader import render_to_string
from django.utils.html import escape
from hashlib import md5
from opengraph import OpenGraph
from urllib.parse import urlparse, parse_qs
from xml.etree import ElementTree as ET
from . import settings
import json
import random
import re
import requests
import string


try:
    from django.core.urlresolvers import reverse
except ImportError:
    from django.urls import reverse


def get_oembed_endpoint(url):
    for (patterns, endpoint, fmt) in settings.URL_PATTERNS:
        if not isinstance(patterns, (list, tuple)):
            patterns = [patterns]

        for pattern in [
            re.compile(
                p.replace(
                    '.', '\\.'
                ).replace(
                    '*', '.*'
                ).replace(
                    '?', '\\?'
                ),
                re.IGNORECASE
            ) for p in patterns
        ]:
            if pattern.match(url) is not None:
                return endpoint, fmt

    return None, None


def get_oembed_response(url, endpoint, fmt, width=settings.WIDTH):
    if fmt == 'json':
        mimetype = 'application/json'
    elif fmt == 'xml':
        mimetype = 'text/xml'
    elif fmt != 'html':  # pragma: no cover
        raise Exception(
            'Handler configured incorrectly (unrecognised format %s)' % fmt
        )

    params = {
        'url': url
    }

    if int(width) > 0:
        params['width'] = width
        params['maxwidth'] = width

    oembed_response = requests.get(
        endpoint,
        params=params,
        headers={
            'Accept': mimetype,
            'User-Agent': 'django'
        }
    )

    if oembed_response.status_code >= 200:
        if oembed_response.status_code < 400:
            return oembed_response.content.decode('utf-8')

    oembed_response.raise_for_status()  # pragma: no cover


def parse_oembed_response(response, fmt):
    if fmt == 'html':
        return response, None, None

    if fmt == 'json':
        data = json.loads(response)

        if 'html' in data:
            return (
                data.get('html'),
                data.get('title'),
                data.get('thumbnail_url')
            )

        raise Exception(
            'Response not understood',
            data
        )  # pragma: no cover

    xml = ET.fromstring(response)
    return (
        xml.find('html').text or '',
        xml.find('title').text or '',
        xml.find('thumbnail_url').text or ''
    )


def get_oembed_content(url, endpoint, fmt, width=None):
    response = get_oembed_response(url, endpoint, fmt, width)
    return parse_oembed_response(response, fmt)


def guess_oembed_content(url, width, inline_images=True):
    headers = requests.head(url).headers
    if headers.get('Content-Type'):
        if headers['Content-Type'].startswith('image/'):
            return (
                '<a href="%s" class="thumbnail" target="_blank">%s</a>' % (
                    escape(url),
                    (
                        '<img class="embedded-image" src="%s" '
                        'style="max-width: 100%%;">'
                    ) % escape(url)
                ),
                '',
                url
            )

    ua = (
        'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) '
        'AppleWebKit/537.36 (KHTML, like Gecko) '
        'Chrome/39.0.2171.95 Safari/537.36'
    )

    accept = (
        'text/html,'
        'application/xhtml+xml,'
        'application/xml;'
        'q=0.9,*/*;q=0.8'
    )

    headers = {
        'Accept': accept,
        'User-Agent': ua,
        'Accept-Language': 'en-US,en;q=0.5',
        'Accept-Encoding': 'gzip, deflate'
    }

    html_response = requests.get(
        url,
        headers=headers
    )

    html_response.raise_for_status()
    html = html_response.content.decode('utf-8')
    matches = settings.LINK_REGEX.findall(html)

    for match in matches:
        attrs = {}
        for attr in settings.ATTR_REGEX.findall(match):
            key, value1, value2 = attr
            attrs[key] = value1 or value2

        if attrs.get('rel') == 'alternate':
            fmt = settings.LINK_TYPE_REGEX.match(attrs.get('type', ''))
            if fmt is not None:
                fmt = fmt.groups()[0]
                url = attrs.get('href')
                urlparts = urlparse(url)
                params = parse_qs(urlparts.query or urlparts.params)
                q = url.find('?')

                if q > -1:
                    url = url[:q]

                params['width'] = width
                params['maxwidth'] = width

                oembed_response = requests.get(
                    url,
                    params=params,
                    headers={
                        'Accept': {
                            'json': 'application/json',
                            'xml': 'text/aml'
                        }[fmt],
                        'User-Agent': 'django'
                    }
                )

                if oembed_response.status_code >= 200:
                    if oembed_response.status_code < 400:
                        return parse_oembed_response(
                            oembed_response.content.decode('utf-8'),
                            fmt
                        )

    graph = OpenGraph(
        html=html,
        scrape=True
    )

    title = graph.get('title')
    image = graph.get('image')

    link = '<p><a href="%s" target="_blank">%s</a></p>' % (
        escape(url),
        escape(url)
    )

    if title:
        link = '<p><a href="%s" target="_blank">%s</a></p>' % (
            escape(url),
            escape(title)
        )

        if image:
            link = (
                '<p><a href="%s" target="_blank">'
                '<img src="%s" max-width="100%%"><br>%s</a></p>'
            ) % (
                escape(url),
                escape(image),
                escape(title)
            )

        return link, title, url

    return None, None, None  # pragma: no cover


def sandbox_iframe(html):
    if html:
        return html.replace(
            '<iframe ',
            '<iframe sandbox="allow-pointer-lock allow-scripts" '
        )

    return html  # pragma: no cover


def make_printable(s):
    printable = set(string.printable)
    return ''.join(
        filter(lambda x: x in printable, s)
    )


def wrap_ajax(url, origin):
    return render_to_string(
        'oembed/placeholder.inc.html',
        {
            'url': url,
            'origin': origin,
            'id': 'oembed_%s' % md5(
                ''.join(
                    url + random.choice(string.ascii_uppercase + string.digits)
                    for i in range(24)
                ).encode('ascii')
            ).hexdigest(),
            'OBJECT_URL': (
                settings.AJAX_OBJECT_URL or reverse('oembed_object')
            )
        }
    )
