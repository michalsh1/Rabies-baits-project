import os
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "Rabies-baits.settings")
import django
django.setup()

from django.db import transaction
from os import listdir
from os.path import isfile, join
import re
from django.contrib.gis.geos import MultiLineString
import os
import rabies_baits_app
from django.contrib.gis.gdal import DataSource
import datetime
from collections import Counter
from rabies_baits_app.models import RoniRoutes, RoniPolygons, Pixel
import json
from django.contrib.gis.geos import GEOSGeometry, Polygon, MultiPolygon


routes_file= "/home/michalsh/projects/Geodjango_play/DATA/roni_routes.json"
with open(routes_file) as f:
    routes_data = json.load(f)
n=0
for feature in routes_data['features']:
    route = GEOSGeometry(str(feature['geometry']))
    route.transform(2039)
    route_properties = feature['properties']
    route_origin = route_properties['route_origin']
    timi_id = route_properties['timi_id']
    timi_related_id = route_properties['timi_related_id']
    date = route_properties['date']
    date_created = route_properties['date_created']
    baits_num = route_properties['baits_num']
    orig_id = route_properties['orig_id']
    origin_files = route_properties['origin_files']
    r= RoniRoutes.objects.create(route=route, route_origin= route_origin, timi_id=timi_id, timi_related_id=timi_related_id, date=date, date_created=date_created, baits_num=baits_num, orig_id=orig_id, origin_files=origin_files)
    n=n+1
    print(n)
    r.save()




polygons_file= "/home/michalsh/projects/Geodjango_play/DATA/roni_polygons.json"
with open(polygons_file) as f2:
    polygons_data = json.load(f2)

n=0
for feature in polygons_data['features']:
    polygon = GEOSGeometry(str(feature['geometry']))
    polygon.transform(2039)
    polygon_properties = feature['properties']
    polygon_origin = polygon_properties['route_origin']
    timi_id = polygon_properties['timi_id']
    date = polygon_properties['date']
    date_created = polygon_properties['date_created']
    baits_num = polygon_properties['baits_num']
    orig_id = polygon_properties['orig_id']
    # origin_files = route_properties['origin_files']
    r= RoniPolygons.objects.create(polygon=polygon, polygon_origin= polygon_origin, timi_id=timi_id, date=date, date_created=date_created, baits_num=baits_num, orig_id=orig_id)
    n=n+1
    print(n)
    r.save()




# import pixels shape

pixel_shp= "/home/michalsh/projects/Rabies-baits/DATA/Red_pixel.shp"
#pixel_shp= "/home/michalsh/projects/Rabies-baits/DATA/red_pixel_reprojecteditm.shp"
ds = DataSource(pixel_shp)
len(ds)
lyr = ds[0]
for feat in lyr:
    poly = feat.geom.geos
    p = Pixel(polygon=poly)
    p.save()
    break




for feat in lyr:
    poly = feat.geom.geos
    print(poly.coords, poly.srid)
    poly.transform(4326)
    print(poly.coords, poly.srid)
    poly.transform(2039)
    print(poly.coords, poly.srid)
    p = Pixel(polygon=poly)
    print(p.polygon.coords, p.polygon.srid)
    p.save()
    print(p.polygon.coords)
    break
###Pixel.objects.all().delete()
