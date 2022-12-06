import datetime
import json
from random import randint
from colormap import rgb2hex

from django.core.serializers import serialize
from django.http import HttpResponse
from django.shortcuts import render
from django.views.generic import TemplateView, FormView, DetailView

from .forms import MyGeoForm, RoniRoutesForm
from .models import Pixel, RoniRoutes



class HomePageView(TemplateView):
        template_name = "baits_app/home.html"


class RoniPageView(TemplateView):
    template_name = "baits_app/roni_data.html"


def roni_pixels(request):
    data = serialize('geojson', Pixel.objects.all())
    return HttpResponse(data, content_type='json')


def RGB(str):
    ## str= 'rgb(red,blue,green)'
    str = str.strip('rgb(').strip(')')
    l = [int(x) for x in str.split(',')]
    t=tuple(l)
    hex = '#%02x%02x%02x' % t
    return hex


def get_color():
    r = randint(1, 255)
    g = randint(1, 255)
    b = randint(1, 255)
    color_tuple = (r, g, b)
    color = 'rgb' + str(color_tuple)
    return color


class RoniRoutesMap(FormView): ###michal - form of hours and days
    form_class = RoniRoutesForm
    template_name = 'baits_app/roni_routes_map.html'

    def get_context_data(self, **kwargs):
        context = super(RoniRoutesMap, self).get_context_data(**kwargs)
        object = RoniRoutes.objects.first()
        context['object'] = object

        if len(self.request.GET) > 0:
            get = dict(self.request.GET)
            days_back = int(get['days_back'][0])
        else:
            days_back = 0

        initial = {'days_back': days_back}
        context['form'] = RoniRoutesForm(initial=initial, instance=object)

        datetime.datetime.today() - datetime.timedelta(days=days_back)

        start_date = datetime.datetime.today()-datetime.timedelta(days=days_back)
        relevant_routes = RoniRoutes.objects.filter(date__gte=start_date)
        context['relevant_routes'] = relevant_routes

        d={}
        for route in relevant_routes:
            route_for_json = RoniRoutes.objects.filter(pk=route.pk)
            route_json = serialize('geojson',
                                         route_for_json,
                                         geometry_field='route',
                                         fields=('pk', 'date', 'baits_num', 'origin_files', 'route_origin', 'timi_id'))
            jsonloads = json.loads(route_json)
            jsonloads['color'] = RGB(get_color())
            jsondumps = json.dumps(jsonloads)

            d[route.pk] = jsondumps
            context['routes_json'] = json.dumps(d) # ind_ils_json

        return context


class MyGeoView(FormView):
    form_class = MyGeoForm
    template_name = "baits_app/geoform.html"

    def get(self, request):
        form = MyGeoForm

        return render(request,
                      self.template_name,
                      {'form': form},
                      )

