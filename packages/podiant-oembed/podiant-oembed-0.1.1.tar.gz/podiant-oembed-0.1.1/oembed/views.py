from django.views.generic.base import View
from django.http.response import HttpResponse
from .models import Resource
from .response import OEmbedResponse
from . import discovery


class OEmbedProviderView(View):
    def get(self, request):
        url = request.GET.get('url')
        if url:
            response = discovery.discover(url)
            if response:
                return response

        return HttpResponse(
            '{"error": "Resource not found"}',
            content_type='application/json',
            status=404
        )


class OEmbedAJAXView(View):
    def get(self, request):
        url = request.GET.get('url')
        callback = request.GET.get('callback')
        resource = Resource.load(url)

        return OEmbedResponse(
            width=resource.width,
            height='auto',
            kind='video',
            title=resource.title,
            html=resource.to_html(),
            jsonp_callback=callback
        )
