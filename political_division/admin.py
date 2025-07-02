from django.contrib import admin
from .models import Provincia, Region, Distrito, Corregimiento, Poblado
from facilities.models import ExtraFieldType, ExtraField
from census.models import Population
from django import forms
from django.forms import ModelForm
from django.contrib.admin.utils import flatten_fieldsets


class ProvinciaForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super(ProvinciaForm, self).__init__(*args, **kwargs)
        for field in ExtraFieldType.objects.filter(model='Provincia'):
            self.fields[field.name] = forms.CharField(required=False)
            self.initial[field.name] = self.get_field(field.name)

    def get_field(self, field_name):
        if (self.instance.pk):
            field_id = ExtraFieldType.objects.filter(name=field_name).first().pk
            extra_field = ExtraField.objects.filter(provincia=self.instance.pk).filter(field_type=field_id).first()
            return '' if extra_field is None else extra_field.value
        else:
            return ''

class ProvinciaAdmin(admin.ModelAdmin):
    form = ProvinciaForm
    list_display = ('provincia',)
    search_fields = ('provincia',)
    fieldsets = (
      ('', {
          'fields': ('provincia', 'cod_prov', 'poligono_id',)
      }),
    )

    def get_form(self, request, obj=None, change=False, **kwargs):
        kwargs['fields'] = flatten_fieldsets(self.fieldsets)
        form = super(ProvinciaAdmin, self).get_form(request, obj, change, **kwargs)

        return form

    def get_fieldsets(self, request, obj=None):
        fieldsets = super(ProvinciaAdmin, self).get_fieldsets(request, obj)
        newfieldsets = list(fieldsets)
        fields = []
        for field in ExtraFieldType.objects.filter(model='Provincia'):
            fields.append(field.name)
        if fields:
            newfieldsets.append(['Metadatos', {'fields': fields}])

        return newfieldsets

    def response_change(self, request, obj):
        provincia_id = request.resolver_match.kwargs['object_id']

        if "_save" in request.POST:
            for field in ExtraFieldType.objects.filter(model='Provincia'):
                if field.name in request.POST:
                    selected_value = request.POST[field.name]
                    field_id = ExtraFieldType.objects.filter(name=field.name).first().pk
                    extra_field = ExtraField.objects.filter(provincia=provincia_id).filter(field_type=field_id).first()
                    if extra_field is None : 
                        extra_field = ExtraField(
                            provincia = Provincia.objects.get(pk=provincia_id),
                            field_type = ExtraFieldType.objects.get(pk=field_id),
                            value = selected_value
                        )
                    else : 
                        extra_field.value = selected_value
                    extra_field.save()
        return super().response_change(request, obj)

    def response_add(self, request, obj, post_url_continue=None):
        if "_save" in request.POST:
            for field in ExtraFieldType.objects.filter(model='Provincia'):
                if field.name in request.POST:
                    selected_value = request.POST[field.name]
                    field_id = ExtraFieldType.objects.filter(name=field.name).first().pk
                    extra_field = ExtraField.objects.filter(provincia=obj.id).filter(field_type=field_id).first()
                    if extra_field is None : 
                        extra_field = ExtraField(
                            provincia = Provincia.objects.get(pk=obj.id),
                            field_type = ExtraFieldType.objects.get(pk=field_id),
                            value = selected_value
                        )
                    else : 
                        extra_field.value = selected_value
                    extra_field.save()
        return super().response_add(request, obj, post_url_continue= post_url_continue)

class RegionForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super(RegionForm, self).__init__(*args, **kwargs)
        for field in ExtraFieldType.objects.filter(model='Region'):
            self.fields[field.name] = forms.CharField(required=False)
            self.initial[field.name] = self.get_field(field.name)

    def get_field(self, field_name):
        if (self.instance.pk):
            field_id = ExtraFieldType.objects.filter(name=field_name).first().pk
            extra_field = ExtraField.objects.filter(region=self.instance.pk).filter(field_type=field_id).first()
            return '' if extra_field is None else extra_field.value
        else:
            return ''

class RegionAdmin(admin.ModelAdmin):
    form = RegionForm
    list_display = ('region', 'provincia')
    search_fields = ('region', )
    fieldsets = (
        ('', {
          'fields': ('provincia', 'region', 'cod_reg',)
        }),
    )

    def get_form(self, request, obj=None, change=False, **kwargs):
        kwargs['fields'] = flatten_fieldsets(self.fieldsets)
        form = super(RegionAdmin, self).get_form(request, obj, change, **kwargs)

        return form

    def get_fieldsets(self, request, obj=None):
        fieldsets = super(RegionAdmin, self).get_fieldsets(request, obj)
        newfieldsets = list(fieldsets)
        fields = []
        for field in ExtraFieldType.objects.filter(model='Region'):
            fields.append(field.name)
        if fields:
            newfieldsets.append(['Metadatos', {'fields': fields}])

        return newfieldsets

    def response_change(self, request, obj):
        region_id = request.resolver_match.kwargs['object_id']

        if "_save" in request.POST:
            for field in ExtraFieldType.objects.filter(model='Region'):
                if field.name in request.POST:
                    selected_value = request.POST[field.name]
                    field_id = ExtraFieldType.objects.filter(name=field.name).first().pk
                    extra_field = ExtraField.objects.filter(region=region_id).filter(field_type=field_id).first()
                    if extra_field is None : 
                        extra_field = ExtraField(
                            region = Region.objects.get(pk=region_id),
                            field_type = ExtraFieldType.objects.get(pk=field_id),
                            value = selected_value
                        )
                    else : 
                        extra_field.value = selected_value
                    extra_field.save()
        return super().response_change(request, obj)

    def response_add(self, request, obj, post_url_continue=None):
        if "_save" in request.POST:
            for field in ExtraFieldType.objects.filter(model='Region'):
                if field.name in request.POST:
                    selected_value = request.POST[field.name]
                    field_id = ExtraFieldType.objects.filter(name=field.name).first().pk
                    extra_field = ExtraField.objects.filter(region=obj.id).filter(field_type=field_id).first()
                    if extra_field is None : 
                        extra_field = ExtraField(
                            region = Region.objects.get(pk=obj.id),
                            field_type = ExtraFieldType.objects.get(pk=field_id),
                            value = selected_value
                        )
                    else : 
                        extra_field.value = selected_value
                    extra_field.save()
        return super().response_add(request, obj, post_url_continue=post_url_continue)

class DistritoForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super(DistritoForm, self).__init__(*args, **kwargs)
        for field in ExtraFieldType.objects.filter(model='Distrito'):
            self.fields[field.name] = forms.CharField(required=False)
            self.initial[field.name] = self.get_field(field.name)

    def get_field(self, field_name):
        if (self.instance.pk):
            field_id = ExtraFieldType.objects.filter(name=field_name).first().pk
            extra_field = ExtraField.objects.filter(distrito=self.instance.pk).filter(field_type=field_id).first()
            return '' if extra_field is None else extra_field.value
        else:
            return ''

class DistritoAdmin(admin.ModelAdmin):
    form = DistritoForm
    list_display = ('distrito', 'region', 'provincia', )
    search_fields = ('distrito', )
    fieldsets = (
      ('', {
          'fields': ('region', 'provincia', 'distrito', 'cod_dist', 'poligono_id', )
      }),
    )

    def get_form(self, request, obj=None, change=False, **kwargs):
        kwargs['fields'] = flatten_fieldsets(self.fieldsets)
        form = super(DistritoAdmin, self).get_form(request, obj, change, **kwargs)

        return form

    def get_fieldsets(self, request, obj=None):
        fieldsets = super(DistritoAdmin, self).get_fieldsets(request, obj)
        newfieldsets = list(fieldsets)
        fields = []
        for field in ExtraFieldType.objects.filter(model='Distrito'):
            fields.append(field.name)
        if fields:
            newfieldsets.append(['Metadatos', {'fields': fields}])

        return newfieldsets

    def response_change(self, request, obj):
        distrito_id = request.resolver_match.kwargs['object_id']

        if "_save" in request.POST:
            for field in ExtraFieldType.objects.filter(model='Distrito'):
                if field.name in request.POST:
                    selected_value = request.POST[field.name]
                    field_id = ExtraFieldType.objects.filter(name=field.name).first().pk
                    extra_field = ExtraField.objects.filter(distrito=distrito_id).filter(field_type=field_id).first()
                    if extra_field is None : 
                        extra_field = ExtraField(
                            distrito = Distrito.objects.get(pk=distrito_id),
                            field_type = ExtraFieldType.objects.get(pk=field_id),
                            value = selected_value
                        )
                    else : 
                        extra_field.value = selected_value
                    extra_field.save()
        return super().response_change(request, obj)

    def response_add(self, request, obj, post_url_continue=None):
        if "_save" in request.POST:
            for field in ExtraFieldType.objects.filter(model='Distrito'):
                if field.name in request.POST:
                    selected_value = request.POST[field.name]
                    field_id = ExtraFieldType.objects.filter(name=field.name).first().pk
                    extra_field = ExtraField.objects.filter(distrito=obj.id).filter(field_type=field_id).first()
                    if extra_field is None : 
                        extra_field = ExtraField(
                            distrito = Distrito.objects.get(pk=obj.id),
                            field_type = ExtraFieldType.objects.get(pk=field_id),
                            value = selected_value
                        )
                    else : 
                        extra_field.value = selected_value
                    extra_field.save()
        return super().response_add(request, obj, post_url_continue= post_url_continue)

class CorregimientoForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super(CorregimientoForm, self).__init__(*args, **kwargs)
        for field in ExtraFieldType.objects.filter(model='Corregimiento'):
            self.fields[field.name] = forms.CharField(required=False)
            self.initial[field.name] = self.get_field(field.name)

    def get_field(self, field_name):
        if (self.instance.pk):
            field_id = ExtraFieldType.objects.filter(name=field_name).first().pk
            extra_field = ExtraField.objects.filter(corregimiento=self.instance.pk).filter(field_type=field_id).first()
            return '' if extra_field is None else extra_field.value
        else:
            return ''

class CorregimientoAdmin(admin.ModelAdmin):
    form = CorregimientoForm
    list_display = ('corregimiento', 'distrito', 'provincia')
    search_fields = ('corregimiento', )
    fieldsets = (
      ('', {
          'fields': ('distrito', 'corregimiento', 'cod_corr', 'poligono_id',)
      }),
    )

    def get_form(self, request, obj=None, change=False, **kwargs):
        kwargs['fields'] = flatten_fieldsets(self.fieldsets)
        form = super(CorregimientoAdmin, self).get_form(request, obj, change, **kwargs)

        return form

    def get_fieldsets(self, request, obj=None):
        fieldsets = super(CorregimientoAdmin, self).get_fieldsets(request, obj)
        newfieldsets = list(fieldsets)
        fields = []
        for field in ExtraFieldType.objects.filter(model='Corregimiento'):
            fields.append(field.name)
        if fields:
            newfieldsets.append(['Metadatos', {'fields': fields}])

        return newfieldsets

    def response_change(self, request, obj):
        corregimiento_id = request.resolver_match.kwargs['object_id']

        if "_save" in request.POST:
            for field in ExtraFieldType.objects.filter(model='Corregimiento'):
                if field.name in request.POST:
                    selected_value = request.POST[field.name]
                    field_id = ExtraFieldType.objects.filter(name=field.name).first().pk
                    extra_field = ExtraField.objects.filter(corregimiento=corregimiento_id).filter(field_type=field_id).first()
                    if extra_field is None : 
                        extra_field = ExtraField(
                            corregimiento = Corregimiento.objects.get(pk=corregimiento_id),
                            field_type = ExtraFieldType.objects.get(pk=field_id),
                            value = selected_value
                        )
                    else : 
                        extra_field.value = selected_value
                    extra_field.save()
        return super().response_change(request, obj)

    def response_add(self, request, obj, post_url_continue=None):
        if "_save" in request.POST:
            for field in ExtraFieldType.objects.filter(model='Corregimiento'):
                if field.name in request.POST:
                    selected_value = request.POST[field.name]
                    field_id = ExtraFieldType.objects.filter(name=field.name).first().pk
                    extra_field = ExtraField.objects.filter(corregimiento=obj.id).filter(field_type=field_id).first()
                    if extra_field is None : 
                        extra_field = ExtraField(
                            corregimiento = Corregimiento.objects.get(pk=obj.id),
                            field_type = ExtraFieldType.objects.get(pk=field_id),
                            value = selected_value
                        )
                    else : 
                        extra_field.value = selected_value
                    extra_field.save()
        return super().response_add(request, obj, post_url_continue= post_url_continue)

class PopulationInline(admin.TabularInline):
    model = Population
    extra = 0
    max_num = 1

class PobladoForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super(PobladoForm, self).__init__(*args, **kwargs)
        for field in ExtraFieldType.objects.filter(model='Poblado'):
            self.fields[field.name] = forms.CharField(required=False)
            self.initial[field.name] = self.get_field(field.name)

    def get_field(self, field_name):
        if (self.instance.pk):
            field_id = ExtraFieldType.objects.filter(name=field_name).first().pk
            extra_field = ExtraField.objects.filter(poblado=self.instance.pk).filter(field_type=field_id).first()
            return '' if extra_field is None else extra_field.value
        else:
            return ''

class PobladoAdmin(admin.ModelAdmin):
    form = PobladoForm
    list_display = ('poblado', 'corregimiento', 'distrito', 'provincia')
    search_fields = ('poblado', )
    inlines = [
        PopulationInline,
    ]
    fieldsets = (
      ('', {
          'fields': ('corregimiento', 'poblado', 'cod_pob', 'contra_key',)
      }),
    )

    def get_form(self, request, obj=None, change=False, **kwargs):
        kwargs['fields'] = flatten_fieldsets(self.fieldsets)
        form = super(PobladoAdmin, self).get_form(request, obj, change, **kwargs)

        return form

    def get_fieldsets(self, request, obj=None):
        fieldsets = super(PobladoAdmin, self).get_fieldsets(request, obj)
        newfieldsets = list(fieldsets)
        fields = []
        for field in ExtraFieldType.objects.filter(model='Poblado'):
            fields.append(field.name)
        if fields:
            newfieldsets.append(['Metadatos', {'fields': fields}])

        return newfieldsets

    def response_change(self, request, obj):
        poblado_id = request.resolver_match.kwargs['object_id']

        if "_save" in request.POST:
            for field in ExtraFieldType.objects.filter(model='Poblado'):
                if field.name in request.POST:
                    selected_value = request.POST[field.name]
                    field_id = ExtraFieldType.objects.filter(name=field.name).first().pk
                    extra_field = ExtraField.objects.filter(poblado=poblado_id).filter(field_type=field_id).first()
                    if extra_field is None : 
                        extra_field = ExtraField(
                            poblado = Poblado.objects.get(pk=poblado_id),
                            field_type = ExtraFieldType.objects.get(pk=field_id),
                            value = selected_value
                        )
                    else : 
                        extra_field.value = selected_value
                    extra_field.save()
        return super().response_change(request, obj)

    def response_add(self, request, obj, post_url_continue=None):
        if "_save" in request.POST:
            for field in ExtraFieldType.objects.filter(model='Poblado'):
                if field.name in request.POST:
                    selected_value = request.POST[field.name]
                    field_id = ExtraFieldType.objects.filter(name=field.name).first().pk
                    extra_field = ExtraField.objects.filter(poblado=obj.id).filter(field_type=field_id).first()
                    if extra_field is None : 
                        extra_field = ExtraField(
                            poblado = Poblado.objects.get(pk=obj.id),
                            field_type = ExtraFieldType.objects.get(pk=field_id),
                            value = selected_value
                        )
                    else : 
                        extra_field.value = selected_value
                    extra_field.save()
        return super().response_add(request, obj, post_url_continue= post_url_continue)
    

admin.site.register(Provincia, ProvinciaAdmin)
admin.site.register(Region, RegionAdmin)
admin.site.register(Distrito, DistritoAdmin)
admin.site.register(Corregimiento, CorregimientoAdmin)
admin.site.register(Poblado, PobladoAdmin)