from django.contrib import admin
from .models import RoniPolygons, RoniRoutes, Pixel, PixelByDate
from leaflet.admin import LeafletGeoAdmin


class RoniPolygonsAdmin(LeafletGeoAdmin):
    list_display = ('pk','orig_id', 'polygon_origin')


class RoniRoutesAdmin(LeafletGeoAdmin):
    list_display = ('pk','orig_id','route_origin', 'origin_files', 'date', 'timi_id')


class PixelAdmin(LeafletGeoAdmin):
    list_display = ('pk', 'baits_count')


class PixelByDateAdmin(LeafletGeoAdmin):
    list_display = ('pk', 'main_pixel', 'date', 'baits_count', 'routesmodel_route', 'polygonmodel_polygon', 'timi_id')


admin.site.register(RoniPolygons, RoniPolygonsAdmin)
admin.site.register(RoniRoutes, RoniRoutesAdmin)
admin.site.register(Pixel, PixelAdmin)
admin.site.register(PixelByDate, PixelByDateAdmin)

