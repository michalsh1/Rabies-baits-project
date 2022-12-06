from os import listdir
from os.path import isfile, join
import re

import django
import pytz
from django.contrib.gis.geos import Point, MultiPoint, MultiLineString, LineString
from django.core.management.base import BaseCommand
import random
import os
from rest_framework import routers, serializers
from django.core.serializers import serialize
from django.core.serializers.json import DjangoJSONEncoder

import rabies_baits_app
from django.contrib.gis.gdal import DataSource, OGRGeometry
from django.contrib.gis.geos import fromstr
import datetime
from collections import Counter

from rabies_baits_app.models import RoniPolygons, RoniRoutes, Pixel, PixelByDate


# ### export all data
class Command(BaseCommand):
    def handle(self, *args, **options):
        ### export RoniPolygons
        json = serialize('geojson',
                         RoniPolygons.objects.all(),
                         geometry_field='polygon',  ## name of field where the geometry to be used
                         fields=('pk', 'route_origin', 'timi_id', 'date', 'date_created', 'baits_num', 'orig_id')
                         )
        return json

        ### export RoniRoutes
        # json = serialize('geojson',
        #                  RoniRoutes.objects.all(),
        #                  geometry_field='route',  ## name of field where the geometry to be used
        #                  fields=('pk', 'route_origin', 'timi_id', 'timi_related_id', 'date', 'date_created', 'baits_num', 'origin_files', 'orig_id')
        #                  )
        # return json


        #

        ### export PixelByDates
        # json = serialize('geojson',
        #                  PixelByDate.objects.all(),
        #                  geometry_field='polygon',  ## name of field where the geometry to be used
        #                  fields=('pk', 'date', 'baits_count', 'routesmodel_route', 'polygonmodel_polygon',
        #                          'orig_id', 'timi_id', 'main_pixel')
        #                  )
        # return json







### export Pixels
        # json = serialize('geojson',
        #                  Pixel.objects.all(),
        #                  geometry_field='polygon',  ## name of field where the geometry to be used
        #                  fields=('pk')
        #                  # fields=('pk', 'baits_count')
        #                  )
        # return json
