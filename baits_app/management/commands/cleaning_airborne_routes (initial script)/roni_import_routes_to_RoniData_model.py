from os import listdir
from os.path import isfile, join
import re

import pytz
from django.contrib.gis.geos import Point, MultiPoint, MultiLineString, LineString
from django.core.management.base import BaseCommand
import random
import os
import rabies_baits_app
from django.contrib.gis.gdal import DataSource, OGRGeometry
from django.contrib.gis.geos import fromstr
import datetime
from collections import Counter

from rabies_baits_app.models import RoniData

list_of_files = []
path = os.path.join(os.path.dirname(rabies_baits_app.__file__), 'ronidata')
files_names = [f for f in listdir(path) if isfile(join(path, f))]
if 'desktop.ini' in files_names:
    files_names.remove('desktop.ini')

# non_files_names = [f for f in listdir(path) if isfile(join(path, f))==False]
created = Counter()
for file in list_of_files:
    created[file]=0

class Command(BaseCommand):
    def handle(self, *args, **options):
        tz = pytz.timezone('UTC')
        no_dates_files = []
        for filename in files_names:
            roni_shp = os.path.abspath(os.path.join(os.path.dirname(rabies_baits_app.__file__),
                                                    'ronidata',
                                                    filename))
            ds = DataSource(roni_shp)

            for i in range(1, len(ds)):
                lyr = ds[i]
                # lyr = ds[2]

                if lyr.name == 'tracks' and lyr.num_feat > 0:
                    for feat in lyr:
                        date = None
                        try:
                            feat_name = feat.get('name')
                        except:
                            feat_name = filename

                        ## check if starts with date (int):
                        try:
                            i0 = feat_name[0]
                            i = int(i0)
                        except ValueError:
                            pass
                        except IndexError:
                            pass

                        ####check for date:

                        ### skip ACTIVE LOGs
                        find_active_logs = re.search(r'ACTIVE LOG', feat_name)
                        if find_active_logs:
                            continue

                        try:
                            find_date = re.search(r'[0-9]{2}-[A-Z]+-[0-9]{2}', feat_name)  ###python3
                            span = find_date.span()
                            date_str = feat_name[span[0]:span[1]]
                            date_time = datetime.datetime.strptime(date_str, '%d-%b-%y')
                            date = date_time.date()
                            # print(date)

                        except AttributeError:  ### if no date found
                            no_dates_files.append(filename)

                        if date!= None:
                            geos_mls_orig = feat.geom.geos
                            roni_new = RoniData(filename=filename,
                                                feat_name=feat_name,
                                                date=date,
                                                mls_orig=geos_mls_orig)
                            roni_new.save()
                            created[filename] += 1

                        else:
                            pass
                            # print("no object created ", feat_name, filename)



        no_dates_files.remove('pt2018__29.4.18__500__490.pgx.gpx')
        no_dates_files.remove('pt2018__30.4.18__244__264.pgx.gpx')
        # print(no_dates_files)
        no_dates_files.remove('pt2018__29.4.18__500__490.pgx.gpx')
        no_dates_files.remove('pt2018__30.4.18__244__264.pgx.gpx')
        # print(no_dates_files)




        # no_dates_files=['050n080n_40ppk.gpx', '060c_40ppk.gpx', '090E30ppk.gpx', '10+40+70+100ppk20box23_14APR20.gpx', '110_30ppk.gpx', '115+145+155ppk15box16_22APR20.gpx', '120130CW40ppk.gpx', '130NE40ppk.gpx', '130_40ppk.gpx', '140_ppk30box9_19APR20.gpx', '15040ppk.gpx', '170N40ppk.gpx', '171+173+181+191ppk20box1_08APR20.gpx', '171+173+181+191ppk20box2_08APR20.gpx', '171+173+181+191ppk20box4_08APR20.gpx', '171173181191ppk20box6.gpx', '171w72w173w_40ppk.gpx', '180+182+192+193+200+211ppk20box15_17APR20.gpx', '20+50+80+100+190ppk20box18_16APR20.gpx', '2017_Boris12_28_11_19_08.gpx', '220+221+222ppk40box11_06APR20.gpx', '220+221+222ppk40box18_06APR20.gpx', '220+221+222ppk40box23_12APR20.gpx', '220+221+222ppk40box3_12APR20.gpx', '230ppk30box8_17APR20.gpx', '231+260+263+265ppk20box12_13APR20.gpx', '240+312+317ppk20box14_19APR.gpx', '241+242+243+245+248ppk40box33_05APR20.gpx', '244+261+262+264ppk30box19_16APR20.gpx', '262+264+267ppk30box13_14APR20.gpx', '266+440+460+480ppk15box12_21APR20.gpx', '266+440+460ppk15box9_22APR20.gpx', '30_60_40k.gpx', '313+330+340+350pp15x10b_05mar.gpx', '313+330+340+350ppk15kmr22.gpx', '35+45ppk15box10_22Mar20.gpx', '360_20ppk3box_30MAR20.gpx', '377+373+370ppk15box11_03APR20.gpx', '410southppk15box1_19_Mar20.gpx', '420+430+410ppk15box9_01APR20.gpx', '420+430ppk15box4_01APR20.gpx', '490+500+510ppk30box18_16APR20.gpx', '500+510ppk30box11_17APR20.gpx', '520+5302oppk.gpx', '540ppk15box6_04mar.gpx', '550+555ppk15box9_16_Mar.gpx', '550+560ppk15box10_12_MAR.gpx', '550+560ppk15box9_15_Mar.gpx', '550ppk15box8_15_Mar.gpx', '550x3west_ppk15box9_08 Mar.gpx', '555+565ppk15box10_23MAR20.gpx', '565-comp-15ppk-3box_02APR20.gpx', '565a+565bppk15box11_30MAR20.gpx', '570+575+615+670ppk15box11_03APR20.gpx', '570ppk15box03_29MAR20 (1).gpx', '570ppk15box7 (1)25_MAR20.gpx', '575+615+670ppk15box4.5_26MAR20.gpx', '575+615+670tpk15box10_25MAR20.gpx', '575, 615, 670Appk15box1_29MAR20.gpx', '575, 615, 670ppk15box8_29MAR20.gpx', '575E-615-15ppk-6box_02APR20.gpx', '600+602+622+623+922ppk15box20_24APR20.gpx', '603+605+921+922ppk15box14_28MAY2020.gpx', '610+690+695ppk15box10_03APR20.gpx', '620+621+625+970ppk15box10_04MAY2020.gpx', '626624685east (1).gpx', '65+75+85+95part1ppk15box9_27MAR20.gpx', '65+75+85+95part2ppk15box9_27MAR20.gpx', '65+75+85+95part3ppk15box3_28MAR20.gpx', '650+660+870ppk15box13.5_23APR20.gpx', '700+705ppk15box9_10_MAR.gpx', '720+560ppk15box9_22MAR20.gpx', '745+25ppk15box10_21_Mar_20.gpx', '745ppk15box0.5_21_Mar20.gpx', '750+710ppk15box9_16_Mar.gpx', '760+800+820ppk15box12_30APR20.gpx', '760ppk15box3_ppk15box3_26APR20.gpx', '770+810ppk15box9_18_Mar_2020.gpx', '780+740ppk15box10_08APR20.gpx', '800+820+830ppk15box7_14MAY2020.gpx', '840+850ppk15box9_09_MAR.gpx', '860+913+917+919+920ppk15box5_28MAR20.gpx', '860+913+917+919+920ppk15box7_28MAR2020.gpx', '905part1ppk15box8_28APR20.gpx', '905part2ppk15box2_28APR20.gpx', '910+911+912+914part1ppk15box_02MAY20.gpx', '910ppk15box9_25APR20.gpx', '911+912+913ppk15box8_12APR20.gpx', '912part2ppk15box_02MAY20.gpx', '918+919+920+921+922ppk15box19_25APR20.gpx', '933+934+937+940x-15ppk-14box-02MAY20.gpx', '933+934ppk15box2_28APR20.gpx', '938+940+941+942ppk15box20_28APR20.gpx', '943+944+945ppk15box10_29APR20.gpx', '945+946+947+948ppk15box11_29APR20.gpx', '949+950+951+952ppk15box10_30APR20.gpx', '950+951+952ppk15box5_30APR20.gpx', '980+931ppk15box12_04MAY2020.gpx', '998+997ppk15box9_07Mar.gpx', 'completion_04APR20.gpx', 'Jordan3a_30ppk8box_30MAR20.gpx', 'Jordan3b_30ppk7box_30MAR20.gpx', 'JordanN-comp-30ppk-3box_02APR20.gpx', 'JordanN1a_25ppk_8box_27MAR20.gpx', 'JordanN1b_25ppk_7box_27Mar20.gpx', 'JordanN2_30ppk_23box_28MAR20.gpx', 'T6.gpx']

        for filename in no_dates_files:
            roni_shp = os.path.abspath(os.path.join(os.path.dirname(rabies_baits_app.__file__),
                                                    'ronidata',
                                                    filename))
            ds = DataSource(roni_shp)
            for i in range(1, len(ds)):
                lyr = ds[i]
                if lyr.name == 'track_points' and lyr.num_feat > 0:
                    for feat in lyr:
                        try:
                            dt_str_orig = str(feat['time'])
                            date = datetime.datetime.strptime(dt_str_orig, '%Y-%m-%d %H:%M:%S').date()
                            if date:
                                # print('yes',filename,lyr, date)
                                break
                        except:
                            continue

            print(date)
            file_date = date
            if file_date:
                for i in range(1, len(ds)):
                    lyr = ds[i]
                    if lyr.name == 'tracks' and lyr.num_feat > 0:
                        # print('---',filename,lyr, file_date)
                        for feat in lyr:
                            try:
                                feat_name = feat.get('name')
                            except:
                                feat_name = filename
                            ### skip ACTIVE LOGs
                            find_active_logs = re.search(r'ACTIVE LOG', feat_name)
                            if find_active_logs:
                                continue

                            geos_mls_orig = feat.geom.geos
                            roni_new = RoniData(filename=filename,
                                                feat_name=feat_name,
                                                date=file_date,
                                                mls_orig=geos_mls_orig)
                            roni_new.save()
                            created[filename] += 1
                            # print('created')
                    date = None

        for k in created.keys():
            print(k, created[k])



