import os
from django.contrib.gis.utils import LayerMapping
# from .models import RatagZones, Parks,  RangerArea

rangerarea_mapping = {
    'id': 'id',
    'area_name': 'area_name',
    'geom': 'MULTIPOLYGON',
}

rangerarea_shp = os.path.abspath(os.path.join(os.path.dirname(__file__), r'data\rangerarea.shp'))


def run(verbose=True):
    lm = LayerMapping(RangerArea, rangerarea_shp, rangerarea_mapping, transform=False, encoding='utf-8')
    lm.save(strict=True, verbose=verbose)
