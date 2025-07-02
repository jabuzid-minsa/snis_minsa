from django.urls import re_path
from . import views


urlpatterns = [
    re_path(r'^regions/(?P<provincia_id>[0-9]+)/$', views.json_regions, name='regions'),
    re_path(r'^distritos/(?P<region_id>[0-9]+)/$', views.json_distritos, name='distritos'),
    re_path(r'^corregimientos/(?P<distrito_id>[0-9]+)/$', views.json_corregimientos, name='corregimientos'),
    re_path(r'^poblados/(?P<corregimiento_id>[0-9]+)/$', views.json_poblados, name='poblados'),
    re_path(r'^delete_instalacion_poblado/(?P<instalacion_id>[0-9]+)/(?P<poblado_id>[0-9]+)/$', views.delete_instalacion_poblado, name='delete_instalacion_poblado'),
]
