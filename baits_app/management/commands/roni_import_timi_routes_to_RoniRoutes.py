import django
from django.db import transaction
django.setup()

from os import listdir
from os.path import isfile, join
from django.contrib.gis.geos import MultiLineString
import os
import rabies_baits_app
from django.contrib.gis.gdal import DataSource
import datetime
from collections import Counter
from rabies_baits_app.models import  RoniRoutes


# class Command(BaseCommand):
#     def handle(self, *args, **options):
def check_and_create_baits_dict():
    ends_obs_baits_dict = dict()
    path = os.path.join(os.path.dirname(rabies_baits_app.__file__), 'Data\\timiroutes\\ends')
    files_names = [f for f in listdir(path) if isfile(join(path, f)) and f.endswith('.shp')]
    if 'desktop.ini' in files_names:
        files_names.remove('desktop.ini')
    timi_ends_path = os.path.abspath(os.path.join(path, files_names[0]))

    timi_ends_ds = DataSource(timi_ends_path)
    timi_ends_lyr=timi_ends_ds[0]

    for feature in timi_ends_lyr:
        num_baits = feature.get('מספר_פ')
        if num_baits == 'None':
            raise ValueError('no baits - check!! ---  ', feature.get('מזהה'))
        else:
            num_baits = int(feature.get('מספר_פ'))
            ends_obs_baits_dict[int(feature.get('מזהה'))] = num_baits

        if num_baits < 10:
            print('number of baits is too low - check!! ---  ', feature.get('מזהה')),
            raise ValueError('number of baits is too low - check!! ---  ', feature.get('מזהה'))

    return ends_obs_baits_dict


def get_timi_related_ob_and_baits(feature, baits_dictionary):
    timi_related_obs_str = feature.get('תצפיו')
    timi_related_obs = list(timi_related_obs_str.split(","))
    timi_related_obs_int = [int(ob_str) for ob_str in timi_related_obs]
    for timi_related_ob in timi_related_obs_int:
        if timi_related_ob in baits_dictionary.keys():
            baits = baits_dictionary[timi_related_ob]
        else:
            continue
        # print(timi_related_ob, baits)

    return [timi_related_ob, baits]


counter = Counter()
pks_list = []
timi_ids = []
baits_dict = check_and_create_baits_dict()

path = os.path.join(os.path.dirname(rabies_baits_app.__file__), 'Data\\timiroutes\\start')
files_names = [f for f in listdir(path) if isfile(join(path, f)) and f.endswith('.shp')]
if 'desktop.ini' in files_names:
    files_names.remove('desktop.ini')
timi_routes_path = os.path.abspath(os.path.join(path,files_names[0]))
timi_routes_ds = DataSource(timi_routes_path)
timi_routes_lyr=timi_routes_ds[0]

with transaction.atomic():
    for feat in timi_routes_lyr:
        counter['timi_obs'] += 1
        date = datetime.date.fromisoformat(feat.get('תאריך_'))
        timi_id = feat.get('מזהה')
        timi_related_ob_and_baits = get_timi_related_ob_and_baits(feat, baits_dict)
        timi_related_ob, baits = timi_related_ob_and_baits
        # print(timi_id,  timi_related_ob, baits)

        if baits is None:
            print('no baits number! ---  ', timi_id)
            raise ValueError

        geos_mls = feat.geom.geos
        geos_mls = MultiLineString(geos_mls, srid=2039)

        ### create object
        roni_new = RoniRoutes(route_origin='1', ##0 = Roni files
                              timi_id=timi_id,
                              timi_related_id=timi_related_ob,
                              date=date,
                              baits_num=baits,
                              # origin_files=tracks.replace('.shp', ''),  ## irrelevant for timi routes
                              route=geos_mls,
                              date_created=datetime.date.today())
        # roni_new.save()
        counter['created routes'] += 1
        pks_list.append(roni_new.pk)
        timi_ids.append(timi_id)

for key, value in counter.items():
    print(key, value)
print(pks_list)
print(timi_ids)