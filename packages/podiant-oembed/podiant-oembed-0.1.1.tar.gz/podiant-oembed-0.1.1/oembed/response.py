from django.http.response import HttpResponse
import json


class OEmbedResponse(HttpResponse):
    def __init__(
        self, kind, width, height, html, version=1.0, title=None,
        jsonp_callback=None
    ):
        super().__init__()

        data = json.dumps(
            {
                'type': kind,
                'html': html,
                'width': width,
                'height': height,
                'version': version,
                'title': title
            }
        )

        if jsonp_callback:
            self.content = '%s(%s)' % (
                jsonp_callback,
                data
            )

            self['Content-Type'] = 'text/javascript'
        else:
            self.content = data
            self['Content-Type'] = 'application/json'
