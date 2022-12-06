from django.urls import path

# from . import views
from .views import HomePageView, MyGeoView, RoniPageView, RoniRoutesMap

urlpatterns = [
     path(r'', HomePageView.as_view(), name="home"),
     path(r'geo_view', MyGeoView.as_view(), name="geo_view"),

     path('roni_data_page', RoniPageView.as_view(), name="home"),
     # path('roni_pixels', roni_pixels, name="roni_pixels"),
     path('roni_routes', RoniRoutesMap.as_view(), name="roni_routes_map"),
 ]



