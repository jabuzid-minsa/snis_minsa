from django.core import serializers
from django.http import HttpResponse
from .models import Provincia, Region, Distrito, Corregimiento, Poblado
from facilities.models import InstalacionPoblado, Instalacion, Poblado
from django.db.models import Q
from django.core.exceptions import ObjectDoesNotExist
import json


def json_regions(request, provincia_id):
    current_provincia = Provincia.objects.get(id=provincia_id)
    regions = Region.objects.all().filter(provincia=current_provincia)
    json_models = serializers.serialize("json", regions)
    return HttpResponse(json_models, content_type="application/javascript")

def json_distritos(request, region_id):
    current_region = Region.objects.get(id=region_id)
    distritos = Distrito.objects.all().filter(region=current_region)
    json_models = serializers.serialize("json", distritos)
    return HttpResponse(json_models, content_type="application/javascript")

def json_corregimientos(request, distrito_id):
    current_distrito = Distrito.objects.get(id=distrito_id)
    corregimientos = Corregimiento.objects.all().filter(distrito=current_distrito)
    json_models = serializers.serialize("json", corregimientos)
    return HttpResponse(json_models, content_type="application/javascript")

def json_poblados(request, corregimiento_id):
    current_corregimiento = Corregimiento.objects.get(id=corregimiento_id)
    poblados = Poblado.objects.all().filter(corregimiento=current_corregimiento)
    json_models = serializers.serialize("json", poblados)
    return HttpResponse(json_models, content_type="application/javascript")

def delete_instalacion_poblado(request, instalacion_id, poblado_id):
    try:
        instalacion = Instalacion.objects.get(id= instalacion_id)
        poblado = Poblado.objects.get(id= poblado_id)
        query = InstalacionPoblado.objects.get(Q(instalacion=instalacion) & Q(poblado=poblado))
        query.delete()
    except ObjectDoesNotExist: 
        return HttpResponse(json.dumps({'code': 500}), status=500, content_type="application/json")
    return HttpResponse(json.dumps({'code': 200}), status=200, content_type="application/json")
