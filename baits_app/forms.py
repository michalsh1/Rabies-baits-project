from django.contrib.gis import forms
from leaflet.forms.fields import PointField

from baits_app.models import RoniRoutes, RoniPolygons


class MyGeoForm(forms.Form):
    point = PointField(widget=forms.OSMWidget(attrs={'map_width': 800, 'map_height': 500}))



class RoniRoutesForm(forms.ModelForm):
    class Meta:
        model = RoniPolygons
        fields = []

    days_back = forms.IntegerField(required=True,
                                   # initial=1,
                                   label=("Days/hours back"),
                                   min_value=1)
