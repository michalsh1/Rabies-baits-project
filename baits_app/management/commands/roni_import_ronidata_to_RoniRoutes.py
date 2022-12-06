import django
from django.db import transaction
django.setup()

from os import listdir
from os.path import isfile, join
import re
from django.contrib.gis.geos import MultiLineString
import os
import rabies_baits_app
from django.contrib.gis.gdal import DataSource
import datetime
from collections import Counter
from rabies_baits_app.models import RoniRoutes


# class Command(BaseCommand):
#     def handle(self, *args, **options):
def get_dates(tracks, path):
    track_points = tracks.replace('tracks.shp',
                                  'track_points.shp')  ## tracks = track layer; track_points = track_points layer
    track_points_path = os.path.abspath(os.path.join(path, track_points))

    track_points_ds = DataSource(track_points_path)
    track_points_lyr = track_points_ds[0]
    date_str = str(track_points_lyr[0]['time'])
    track_points_date = datetime.date.fromisoformat(date_str)
    return track_points_date


def get_geometry(tracks, path):
    tracks_path = os.path.abspath(os.path.join(path, tracks))
    tracks_ds = DataSource(tracks_path)
    tracks_lyr = tracks_ds[0]
    geom = tracks_lyr[0].geom.clone()
    geom.coord_dim = 2
    geom_geos = geom.geos
    if geom_geos.srid == 4326:
        if geom_geos.geom_type!='MultiLineString':
            geos_mls = MultiLineString(geom_geos, srid=4326)
        else:
            geos_mls=geom_geos
        geos_mls.transform(2039)

    elif geom_geos.srid == 2039:
        if geom_geos.geom_type!='MultiLineString':
            geos_mls = MultiLineString(geom_geos, srid=2039)
        else:
            geos_mls=geom_geos
    else:
        raise ValueError
    return geos_mls


def get_baits(tracks):
    try:
        box_match = re.search(r'Box(\d+\.\d+)', tracks) or re.search(r'Box(\d+)', tracks)
        boxes_num = float(box_match.group(1))
    except AttributeError:
        print("no number after 'Box'")

    baits = boxes_num*360
    baits = round(baits)
    return baits


counter = Counter()
pks_list = []
files_processed = []

path = os.path.join(os.path.dirname(rabies_baits_app.__file__), 'Data\\ronidata')
files_names = [f for f in listdir(path) if isfile(join(path, f)) and f.endswith('tracks.shp')]
if 'desktop.ini' in files_names:
    files_names.remove('desktop.ini')

with transaction.atomic():
    for tracks in files_names:
        counter['files'] += 1
        date = get_dates(tracks, path)
        geos_mls = get_geometry(tracks, path)
        baits = get_baits(tracks)

        ### create object
        roni_new = RoniRoutes(route_origin='0', ##0 = Roni files
                              # timi_id='', ## irrelevant for roni files
                              # timi_related_id='', ## irrelevant for roni files
                              date=date,
                              baits_num=baits,
                              origin_files=tracks.replace('.shp', ''),
                              route=geos_mls,
                              date_created=datetime.date.today())
        roni_new.save()
        counter['created routes'] += 1
        pks_list.append(roni_new.pk)
        files_processed.append(tracks.replace('.shp', ''))

for key, value in counter.items():
    print(key, value)
print(pks_list)
print(files_processed)