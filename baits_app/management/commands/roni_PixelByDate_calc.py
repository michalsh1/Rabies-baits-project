import os
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "Rabies-baits.settings")
import django
django.setup()

from django.db import transaction

from os import listdir
from os.path import isfile, join
import re

import pytz
from django.contrib.gis.geos import Point, MultiPoint, MultiLineString, LineString, MultiPolygon
from django.core.management.base import BaseCommand
import random
import os
import rabies_baits_app
from django.contrib.gis.gdal import DataSource, OGRGeometry
from django.contrib.gis.geos import fromstr
import datetime
from collections import Counter

from rabies_baits_app.models import RoniRoutes, RoniPolygons, Pixel, PixelByDate


# PixelByDate calculation:
# class Command(BaseCommand):
#     def handle(self, *args, **options):

def baits_per_pixel_calc(route_obj):
    pixel_count = 0
    if isinstance(route_obj, RoniRoutes):
        geometry = route_obj.route
    elif isinstance(route_obj, RoniPolygons):
        geometry = route_obj.polygon
    geometry.transform(4326)
    for p in Pixel.objects.all():
        pixel = p.polygon
        if geometry.intersects(pixel):
            pixel_count += 1  # number of pixels that intersects with this route
    if pixel_count>0:
        baits_per_pixel_result = route_obj.baits_num / pixel_count   # Average
    else:
        baits_per_pixel_result=0
    return baits_per_pixel_result


pixel_objects = Pixel.objects.all()
today = datetime.date.today()
counter = Counter()
counter['processed_routes'] = 0
counter['processed_polygons'] = 0

routes_set = set()
for pbd in PixelByDate.objects.all():
    routes_set.add(pbd.routesmodel_route_id)

polygons_set = set()
for pbd in PixelByDate.objects.all():
    polygons_set.add(pbd.polygonmodel_polygon_id)

# for i, route_obj in enumerate(RoniRoutes.objects.all()):
#     print('new route: ', route_obj.pk)
#     baits_per_pixel = baits_per_pixel_calc(route_obj)
#     print(baits_per_pixel)

with transaction.atomic():
    print('ROUTES:')
    for i, route_obj in enumerate(RoniRoutes.objects.all()):
        if i % 100 == 0:
            print(i, "/ ", len(RoniRoutes.objects.all()))
        if route_obj.pk in routes_set:  # so that if it was already calculated- don't calculate again
            pass
        else:
            print('new route: ', route_obj.pk)
            route_date = route_obj.date
            route_geom = route_obj.route
            route_orig_id = route_obj.orig_id
            route_timi_id = route_obj.timi_id
            route_timi_related_id = route_obj.timi_related_id
            baits_per_pixel = baits_per_pixel_calc(route_obj)
            print(baits_per_pixel)
            for p in pixel_objects:
                pixel_polygon = p.polygon
                if route_geom.intersects(pixel_polygon):
                    route_pbd = PixelByDate(main_pixel=p,
                                            baits_count=baits_per_pixel,
                                            date=route_date,
                                            routesmodel_route=route_obj,
                                            orig_id=route_orig_id,
                                            timi_id=route_timi_id,
                                            timi_related_id=route_timi_related_id,
                                            date_calculated=today,
                                            polygon=pixel_polygon)
                    route_pbd.save()
            counter['processed_routes'] += 1
    print('\n')

    print('\n')

    print('\n')

    print('\n')

    print('---------------')
    print('POLYGONS:')
    for x, polygon_obj in enumerate(RoniPolygons.objects.all()):
        if x % 10 == 0:
            print(x, "/ ", len(RoniPolygons.objects.all()))
        if polygon_obj.pk in polygons_set:
            pass
        else:
            print('new polygon: ', polygon_obj.pk)
            polygon_geom = polygon_obj.polygon
            polygon_orig_id = polygon_obj.orig_id
            polygon_timi_id = polygon_obj.timi_id
            polygon_date = polygon_obj.date
            baits_per_pixel = baits_per_pixel_calc(polygon_obj)
            for p in pixel_objects:
                pixel_polygon = p.polygon
                if polygon_geom.intersects(pixel_polygon):
                    polygon_pbd = PixelByDate(main_pixel=p,
                                              baits_count=baits_per_pixel,
                                              date=polygon_date,
                                              polygonmodel_polygon=polygon_obj,
                                              orig_id=polygon_orig_id,
                                              timi_id=polygon_timi_id,
                                              date_calculated=today,
                                              polygon=pixel_polygon)
                    polygon_pbd.save()
                    print(polygon_pbd.pk)
            counter['processed_polygons'] += 1
print('\n')

print('\n')

print('---------------------')
print('Done!')
for key, value in counter.items():
    print(key,': ', value)



