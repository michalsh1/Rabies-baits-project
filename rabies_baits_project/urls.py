
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    # path('admin/', admin_urls),
    path(r'', include('baits_app.urls'))
]
