from django.conf import settings as site_settings
from os import path
import json
import logging
import re


def load_providers():
    filename = path.join(
        path.dirname(__file__),
        'fixtures',
        'providers.json'
    )

    return json.load(open(filename, 'rb'))


WIDTH = getattr(site_settings, 'OEMBED_WIDTH', 640)
SANDBOX = getattr(site_settings, 'SANDBOX', False)
URL_PATTERNS = list(
    getattr(site_settings, 'OEMBED_URLPATTERNS', [])
) + load_providers()

CACHE_PREFIX = getattr(site_settings, 'OEMBED_CACHE_PREFIX', 'oembed_')
CACHE_TIMEOUT = getattr(
    site_settings,
    'OEMBED_CACHE_TIMEOUT',
    getattr(site_settings, 'CACHES', {}).get('default', {}).get('TIMEOUT', 300)
)

AJAX_OBJECT_URL = getattr(
    site_settings,
    'OEMBED_AJAX_OBJECT_URL',
    None
)

P_REGEX = re.compile(
    r'<p>([^<]+)<\/p>', re.IGNORECASE
)

LINK_REGEX = re.compile(r'\<link[^\>]+\>', re.IGNORECASE)
ATTR_REGEX = re.compile(
    r""" ([a-z]+)=(?:"([^"]+)"|'([^']+)')""",
    re.IGNORECASE
)

LINK_TYPE_REGEX = re.compile(r'^application/(json|xml)\+oembed$')
OEMBED_LOGGER = logging.getLogger('oembed')


__all__ = [
    'ATTR_REGEX',
    'CACHE_PREFIX',
    'CACHE_TIMEOUT',
    'LINK_REGEX',
    'LINK_TYPE_REGEX',
    'OEMBED_LOGGER',
    'P_REGEX',
    'SANDBOX',
    'URL_PATTERNS',
    'WIDTH'
]
