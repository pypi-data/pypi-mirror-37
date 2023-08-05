from .discoverers import DiscovererList
from .parse import parse_html


__version__ = '0.1.1'
__all__ = [
    'parse_html',
    'discovery'
]


default_app_config = 'oembed.apps.OembedAppConfig'


discovery = DiscovererList()
