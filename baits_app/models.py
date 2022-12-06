from __future__ import unicode_literals

from django.contrib.gis.db import models
from django.contrib.gis.db.models import MultiLineStringField, MultiPolygonField, MultiPointField, LineStringField, GeometryCollectionField
from django.core.serializers import serialize

from django.db.models import Manager as GeoManager

ITM_SRID = 2039
ICS_SRID = 28193
UTM_SRID = 32636
WGS84_SRID = 4326


class Origin(object):
    RONI_FILES = 0
    TIMI = 1

    choices = (
        (RONI_FILES, ('Ronis files')),
        (TIMI, ('Timi')),
    )


class RoniPolygons(models.Model):
    polygon_origin = models.IntegerField(choices=Origin.choices, null=True, blank=True)
    timi_id = models.IntegerField(null=True, blank=True)
    date = models.DateField(null=True, blank=True)
    date_created = models.DateField(null=True, blank=True)
    polygon = MultiPolygonField(null=True, blank=True, srid=ITM_SRID)
    baits_num = models.IntegerField(null=True, blank=True)
    orig_id = models.IntegerField(null=True, blank=True, unique=True) ##only for roni's data.. - its the id in the excel data

    def __str__(self):
        return str(self.pk)


class RoniRoutes(models.Model):
    route_origin = models.IntegerField(choices=Origin.choices, null=True, blank=True)
    timi_id = models.IntegerField(null=True, blank=True)
    timi_related_id = models.IntegerField(null=True, blank=True)
    date = models.DateField(null=True, blank=True)
    date_created = models.DateField(null=True, blank=True)
    baits_num = models.IntegerField(null=True, blank=True)
    orig_id = models.IntegerField(null=True, blank=True, unique=True) ##only fot roni's data.. - its the id in the excel data
    origin_files = models.CharField(max_length=500, null=True, blank=True) ##only fot roni's data..
    route = MultiLineStringField(null=True, blank=True, srid=ITM_SRID)



class Pixel(models.Model):
    polygon = models.PolygonField(null=True)
    # polygon_wsg = models.PolygonField(srid=WGS84_SRID)
    baits_count = models.FloatField(null=True, blank=True,  verbose_name='Baits count')


class PixelByDate(models.Model):
    polygon = models.PolygonField(null=True, blank=True)
    baits_count = models.FloatField(null=True, blank=True,  verbose_name='Baits count')
    date = date = models.DateField(null=True, blank=True)
    date_calculated = models.DateField(null=True, blank=True)
    main_pixel = models.ForeignKey(Pixel, related_name='pixel_by_date', on_delete=models.CASCADE, blank=True, null=True)
    routesmodel_route = models.ForeignKey(RoniRoutes, related_name='pixels_by_date', on_delete=models.CASCADE, blank=True, null=True)
    polygonmodel_polygon = models.ForeignKey(RoniPolygons, related_name='pixels_by_date', on_delete=models.CASCADE, blank=True, null=True)
    orig_id = models.IntegerField(null=True, blank=True, unique=False)
    timi_id = models.IntegerField(null=True, blank=True)
    timi_related_id = models.IntegerField(null=True, blank=True)
    original_filename = models.CharField(max_length=50, null=True, blank=True, unique=True)





