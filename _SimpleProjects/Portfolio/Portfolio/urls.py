from django.contrib import admin
from django.urls import path, include

from django.conf.urls import include, url
from purview import views

urlpatterns = [
    path('purview/', include('purview.urls')), 
    path('admin/', admin.site.urls),
]
