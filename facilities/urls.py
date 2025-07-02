from django.urls import path, re_path
from . import views
from django.contrib.auth.decorators import login_required, permission_required


app_name = 'facilities'

urlpatterns = [
    path('', login_required(views.UnidadesCriticasListView.as_view()), name='index'),
    path('uc/add/', login_required(views.UnidadesCriticasCreate.as_view()), name='uc-add'),
    path('uc/list/', login_required(views.UnidadesCriticasListView.as_view()), name='uc-list'),
    re_path(r'uc/detail/(?P<pk>[0-9]+)/$', login_required(views.UnidadesCriticasDetail.as_view()), name='uc-detail'),
    re_path(r'uc/update/(?P<pk>[0-9]+)/$', login_required(views.UnidadesCriticasUpdate.as_view()), name='uc-update'),
    re_path(r'uc/delete/(?P<pk>[0-9]+)/$', login_required(views.UnidadesCriticasDelete.as_view()), name='uc-delete'),
    path('instalacion-autocomplete/', login_required(views.InstalacionAutocomplete.as_view()), name='instalacion-autocomplete'),
    path('ajax/load-distritos/', login_required(views.load_distritos), name='load-distritos'),
    path('ajax/load-corregimientos/', login_required(views.load_corregimientos), name='load-corregimientos'),

    path('ajax/approve-report/', login_required(views.approve_report), name='approve_report'),
    path('reportes-covid/', login_required(views.export_xls), name='export_xls'),
]
