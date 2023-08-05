from .discoverers import DiscovererList
from .parse import parse_html


__version__ = '0.2.0'
__all__ = [
    'parse_html',
    'discovery'
]


default_app_config = 'oembed.apps.OembedAppConfig'


discovery = DiscovererList()
