import django
from django.db import transaction
django.setup()

from os import listdir
from os.path import isfile, join
from django.contrib.gis.geos import Point, MultiPolygon
import os
import rabies_baits_app
from django.contrib.gis.gdal import DataSource
from collections import Counter
from datetime import datetime
from rabies_baits_app.models import RoniPolygons


# class Command(BaseCommand):
#     def handle(self, *args, **options):
def create_polygon(feat):
    coords = feat.geom.coords[0]
    point = Point(coords[0], coords[1], srid=2039)
    polygon = point.buffer(30)
    mp = MultiPolygon(polygon)
    return mp


counter = Counter()
pks_list=[]
timi_ids = []

path = os.path.join(os.path.dirname(rabies_baits_app.__file__), 'Data\\timipoints')
files_names = [f for f in listdir(path) if isfile(join(path, f)) and f.endswith('.shp')]
if 'desktop.ini' in files_names:
    files_names.remove('desktop.ini')
timi_points = files_names[0]
timi_points_path = os.path.abspath(os.path.join(path, timi_points))
timi_points_ds = DataSource(timi_points_path)


with transaction.atomic():
    lyr=timi_points_ds[0]
    for feat in lyr:
        counter['timi_obs'] += 1
        timi_id = feat.get('מזהה')
        date = feat.get('תאריך_')
        baits = feat.get('מספר_פ')
        if baits is None:
            print('no baits number! ---  ', timi_id)
            raise ValueError
        polygon = create_polygon(feat)
        print(timi_id, date, baits)

        #### create object
        roni_new = RoniPolygons(route_origin=1,
                                timi_id=timi_id, ## irrelevant for roni files
                                date=date,
                                polygon=polygon,
                                baits_num=baits,
                                date_created=datetime.date.today())
        # roni_new.save()
        counter['created polygons'] += 1
        pks_list.append(roni_new.pk)
        timi_ids.append(timi_id)

for key, value in counter.items():
    print(key, value)
print(pks_list)
print(timi_ids)