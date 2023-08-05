from django.http.response import HttpResponse
from django.views.generic.base import View
from . import get_tour_data, save_tour_data
import json


class TourDataView(View):
    http_method_names = ('get', 'post')

    def get(self, request):
        return HttpResponse(
            json.dumps(
                get_tour_data(request)
            ),
            content_type='application/json'
        )

    def post(self, request):
        data = request.POST.get('data', '{}')
        data = json.loads(data)

        save_tour_data(request, data)
        return HttpResponse(
            'true',
            content_type='application/json'
        )
