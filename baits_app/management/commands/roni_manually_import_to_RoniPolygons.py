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
import datetime
from rabies_baits_app.models import RoniPolygons


# class Command(BaseCommand):
#     def handle(self, *args, **options):

path = os.path.join(os.path.dirname(rabies_baits_app.__file__), 'Data\\manually_import_polygon')
files_names = [f for f in listdir(path) if isfile(join(path, f)) and f.endswith('.shp')]
if 'desktop.ini' in files_names:
    files_names.remove('desktop.ini')
new_polygon = files_names[0]
new_polygon_path = os.path.abspath(os.path.join(path, new_polygon))
new_polygon_ds = DataSource(new_polygon_path)


with transaction.atomic():
    lyr=new_polygon_ds[0]
    for feat in lyr:
        polygon = lyr[0].geom.geos
        mp = MultiPolygon(polygon, srid=2039)


        #### create object
        roni_new = RoniPolygons(polygon=mp,
                                date_created=datetime.date.today()
                                )
        # roni_new.save()
        print(roni_new.pk)

