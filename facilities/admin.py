from django.contrib import admin, messages
from django.http import HttpResponseRedirect
from .models import Dependencia, TipoInstalacion, Nivel, Instalacion, InstalacionPoblado, Servicio, Horario, Phone, Employee, Position, ExtraField, ExtraFieldType, Profesion, Especialidad, UnidadesCriticas
from political_division.models import Provincia, Poblado
from django.db.models import Subquery
from django import forms
from django.forms import ModelForm
from django_admin_listfilter_dropdown.filters import DropdownFilter, RelatedDropdownFilter, ChoiceDropdownFilter


from django.contrib.admin.utils import flatten_fieldsets

class ServicioAdmin(admin.ModelAdmin):
    pass

class HorarioInline(admin.TabularInline):
    model = Horario
    extra = 0

class PhoneInline(admin.TabularInline):
    model = Phone
    extra = 0
    fields = ["number", "phone_choise"]

class InstalacionForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super(InstalacionForm, self).__init__(*args, **kwargs)
        for field in ExtraFieldType.objects.filter(model='Instalacion'):
            self.fields[field.name] = forms.CharField(required=False)
            self.initial[field.name] = self.get_field(field.name)

    def get_field(self, field_name):
        if (self.instance.pk):
            field_id = ExtraFieldType.objects.filter(name=field_name).first().pk
            extra_field = ExtraField.objects.filter(instalacion=self.instance.pk).filter(field_type=field_id).first()
            return '' if extra_field is None else extra_field.value
        else:
            return ''

class InstalacionAdmin(admin.ModelAdmin):
    form = InstalacionForm

    list_display = ('instalacion', 'tipo_instalacion',)
    search_fields = ('instalacion',)
    readonly_fields = ()

    fieldsets = (
      ('', {
          'fields': ('corregimiento', 'dependencia', 'tipo_instalacion', 'region_dependencia', 'nivel', 'instalacion',
          'cod_inst', 'latitude', 'longitude', 'servicios', 'observaciones',)
      }),
    )

    inlines = [
        HorarioInline,
        PhoneInline,
    ]
    filter_horizontal = ('servicios',)

    def get_form(self, request, obj=None, change=False, **kwargs):
        kwargs['fields'] = flatten_fieldsets(self.fieldsets)
        form = super(InstalacionAdmin, self).get_form(request, obj, change, **kwargs)

        return form

    def get_fieldsets(self, request, obj=None):
        fieldsets = super(InstalacionAdmin, self).get_fieldsets(request, obj)
        newfieldsets = list(fieldsets)
        fields = []
        for field in ExtraFieldType.objects.filter(model='Instalacion'):
            fields.append(field.name)
        if fields:
            newfieldsets.append(['Metadatos', {'fields': fields}])

        return newfieldsets

    def add_view(self, request, form_url='', extra_context=None):
        return super(InstalacionAdmin, self).add_view(request, form_url=form_url, extra_context=extra_context)

    def change_view(self, request, object_id, form_url='', extra_context=None):
        instalacion_id = request.resolver_match.kwargs['object_id']
        if extra_context is None:
            provincias = Provincia.objects.all()
            poblados_by_instalacion = InstalacionPoblado.objects.filter(instalacion=instalacion_id)
            poblado_list = Poblado.objects.filter(id__in = Subquery(poblados_by_instalacion.values('poblado_id')))
            extra_context = {"provincia_list": provincias, "instalacion_id": instalacion_id, "poblado_list":poblado_list, "change_view": True}
        return super(InstalacionAdmin, self).change_view(
            request, object_id=object_id, form_url=form_url, extra_context=extra_context)

    def response_change(self, request, obj):
        instalacion_id = request.resolver_match.kwargs['object_id']

        if "_add-poblado" in request.POST:
            if 'poblado' in request.POST:
                selected_value = request.POST["poblado"] 
                if selected_value:
                    instalacion_poblado = InstalacionPoblado()
                    instalacion_poblado.instalacion = Instalacion.objects.get(pk=instalacion_id)
                    instalacion_poblado.poblado = Poblado.objects.get(pk=selected_value)
                    instalacion_poblado.save()
                    self.message_user(request, "Poblado agregado", level=messages.SUCCESS)
            else:
                self.message_user(request, "Poblado no agregado", level=messages.ERROR)
            return HttpResponseRedirect(".")
        elif "_save" in request.POST:
            for field in ExtraFieldType.objects.filter(model='Instalacion'):
                if field.name in request.POST:
                    selected_value = request.POST[field.name]
                    field_id = ExtraFieldType.objects.filter(name=field.name).first().pk
                    extra_field = ExtraField.objects.filter(instalacion=instalacion_id).filter(field_type=field_id).first()
                    if extra_field is None : 
                        extra_field = ExtraField(
                            instalacion = Instalacion.objects.get(pk=instalacion_id),
                            field_type = ExtraFieldType.objects.get(pk=field_id),
                            value = selected_value
                        )
                    else : 
                        extra_field.value = selected_value
                    extra_field.save()
        return super().response_change(request, obj)

    def response_add(self, request, obj, post_url_continue=None):
        if "_save" in request.POST:
            for field in ExtraFieldType.objects.filter(model='Instalacion'):
                if field.name in request.POST:
                    selected_value = request.POST[field.name]
                    field_id = ExtraFieldType.objects.filter(name=field.name).first().pk
                    extra_field = ExtraField.objects.filter(instalacion=obj.id).filter(field_type=field_id).first()
                    if extra_field is None : 
                        extra_field = ExtraField(
                            instalacion = Instalacion.objects.get(pk=obj.id),
                            field_type = ExtraFieldType.objects.get(pk=field_id),
                            value = selected_value
                        )
                    else : 
                        extra_field.value = selected_value
                    extra_field.save()
        return super().response_add(request, obj, post_url_continue= post_url_continue)

class PositionAdmin(admin.ModelAdmin):
    list_display = ('position',)
    search_fields = ('position',)

class EmployeeForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super(EmployeeForm, self).__init__(*args, **kwargs)
        for field in ExtraFieldType.objects.filter(model='Employee'):
            self.fields[field.name] = forms.CharField(required=False)
            self.initial[field.name] = self.get_field(field.name)

    def get_field(self, field_name):
        if (self.instance.pk):
            field_id = ExtraFieldType.objects.filter(name=field_name).first().pk
            extra_field = ExtraField.objects.filter(employee=self.instance.pk).filter(field_type=field_id).first()
            return '' if extra_field is None else extra_field.value
        else:
            return ''

class EmployeeAdmin(admin.ModelAdmin):
    form = EmployeeForm

    list_display = ('name', 'last_name', 'identity_card', 'job_position', )
    search_fields = ('name', 'last_name', 'identity_card',)
    readonly_fields = ()

    fieldsets = (
      ('', {
          'fields': ('id_minsa', 'name', 'last_name', 'identity_card', 'job_position', 'salary',
          'start_date', 'spend_object', 'status', 'especialidades', 'instalaciones', 'observaciones',)
      }),
    )
    filter_horizontal = ('especialidades','instalaciones',)
    
    inlines = [
        PhoneInline,
    ]

    def get_form(self, request, obj=None, change=False, **kwargs):
        kwargs['fields'] = flatten_fieldsets(self.fieldsets)
        form = super(EmployeeAdmin, self).get_form(request, obj, change, **kwargs)

        return form

    def get_fieldsets(self, request, obj=None):
        fieldsets = super(EmployeeAdmin, self).get_fieldsets(request, obj)
        newfieldsets = list(fieldsets)
        fields = []
        for field in ExtraFieldType.objects.filter(model='Employee'):
            fields.append(field.name)
        if fields:
            newfieldsets.append(['Metadatos', {'fields': fields}])

        return newfieldsets

    def response_change(self, request, obj):
        employee_id = request.resolver_match.kwargs['object_id']

        if "_save" in request.POST:
            for field in ExtraFieldType.objects.filter(model='Employee'):
                if field.name in request.POST:
                    selected_value = request.POST[field.name]
                    field_id = ExtraFieldType.objects.filter(name=field.name).first().pk
                    extra_field = ExtraField.objects.filter(employee=employee_id).filter(field_type=field_id).first()
                    if extra_field is None : 
                        extra_field = ExtraField(
                            employee = Employee.objects.get(pk=employee_id),
                            field_type = ExtraFieldType.objects.get(pk=field_id),
                            value = selected_value
                        )
                    else : 
                        extra_field.value = selected_value
                    extra_field.save()
        return super().response_change(request, obj)

    def response_add(self, request, obj, post_url_continue=None):
        if "_save" in request.POST:
            for field in ExtraFieldType.objects.filter(model='Employee'):
                if field.name in request.POST:
                    selected_value = request.POST[field.name]
                    field_id = ExtraFieldType.objects.filter(name=field.name).first().pk
                    extra_field = ExtraField.objects.filter(employee=obj.id).filter(field_type=field_id).first()
                    if extra_field is None : 
                        extra_field = ExtraField(
                            employee = Employee.objects.get(pk=obj.id),
                            field_type = ExtraFieldType.objects.get(pk=field_id),
                            value = selected_value
                        )
                    else : 
                        extra_field.value = selected_value
                    extra_field.save()
        return super().response_add(request, obj, post_url_continue= post_url_continue)

class ExtraFieldTypeAdmin(admin.ModelAdmin):
    list_display = ('name', 'description', 'model')
    search_fields = ('name', )
    readonly_fields = ()

class UnidadesCriticasForm(ModelForm):

    def __init__(self, *args, **kwargs):
        super(UnidadesCriticasForm, self).__init__(*args, **kwargs)
        for field in ExtraFieldType.objects.filter(model='UnidadesCriticas'):
            self.fields[field.name] = forms.CharField(required=False)
            self.initial[field.name] = self.get_field(field.name)

    def get_field(self, field_name):
        if (self.instance.pk):
            field_id = ExtraFieldType.objects.filter(name=field_name).first().pk
            extra_field = ExtraField.objects.filter(unidades_criticas=self.instance.pk).filter(field_type=field_id).first()
            return '' if extra_field is None else extra_field.value
        else:
            return ''

    class Meta:
        model = UnidadesCriticas
        fields = '__all__'
        widgets = {
          'observaciones': forms.Textarea(attrs={'rows':15, 'cols':70}),
          'observaciones_camas': forms.Textarea(attrs={'rows':15, 'cols':70}),
          'observaciones_rh': forms.Textarea(attrs={'rows':15, 'cols':70}),
        }

class UnidadesCriticasAdmin(admin.ModelAdmin):
    form = UnidadesCriticasForm
    autocomplete_fields = ['instalacion']

    list_display = ('instalacion','reg_date','aprobado', 'camas_uci','camas_semi','camas_sala','camas_covid','camas_covid_sala',
    'camas_otro','camas_otro_sala','vent_dispo','vent_dispo_trans','vent_dispo_fijo','pacientes_vma','pacientes_vma_trans',
    'pacientes_vma_fijo','pacientes_vma_semi','pacientes_vma_semi_trans','pacientes_vma_semi_fijo','pacientes_vma_sala','pacientes_vma_sala_trans','pacientes_vma_sala_fijo', 'vent_otro', 'vent_otro_trans', 
    'vent_otro_fijo','pacientes_covid_int','pacientes_covid_ext','pacientes_traslado','defunciones_covid', 'intensivistas',
    'intensivistas_dispo', 'internistas','internistas_dispo', 'infectologos', 'infectologos_dispo','anestesiologos', 'anestesiologos_dispo', 
    'neumologos','neumologos_dispo','cirujanos','cirujanos_dispo','enfermeros', 'enfermeros_dispo','tecnicos', 'tecnicos_dispo',
    'terapistas_resp','terapistas_resp_dispo','pacientes_uci','pacientes_uci_otro','ventiladores','ventilados_otro', 'intubados',
    'extubados','egresos_uci','ingresos', 'muertes',)
    search_fields = ('instalacion__instalacion',)
    date_hierarchy = ('reg_date')
    fieldsets = (
      ('', {
          'fields': ('instalacion', 'reg_date', 'aprobado' )
      }),
      ('CAMAS UCI', {'fields':('camas_uci','camas_semi','camas_sala','camas_covid','camas_covid_sala','camas_otro','camas_otro_sala',
      ('vent_dispo','vent_dispo_trans','vent_dispo_fijo'),('pacientes_vma','pacientes_vma_trans','pacientes_vma_fijo'),
      ('pacientes_vma_semi','pacientes_vma_semi_trans','pacientes_vma_semi_fijo'),
      ('pacientes_vma_sala','pacientes_vma_sala_trans','pacientes_vma_sala_fijo'), ('vent_otro', 'vent_otro_trans', 'vent_otro_fijo'), 
      'pacientes_covid_int','pacientes_covid_ext','pacientes_traslado','defunciones_covid', 'observaciones_camas')}),
      ('RECURSOS HUMANOS PARA UCI', {'fields':(('intensivistas','intensivistas_dispo'), ('internistas','internistas_dispo'), 
      ('infectologos', 'infectologos_dispo'),('anestesiologos', 'anestesiologos_dispo'), ('neumologos','neumologos_dispo'),
      ('cirujanos','cirujanos_dispo'),('enfermeros', 'enfermeros_dispo'),('tecnicos', 'tecnicos_dispo'),
      ('terapistas_resp','terapistas_resp_dispo'),'observaciones_rh')}),
      ('DATOS EXTRAS', {'fields':('pacientes_uci','pacientes_uci_otro','ventiladores','ventilados_otro', 'intubados','extubados',
      'egresos_uci','ingresos', 'muertes', 'observaciones',)}),
    )

    #def info_display(self, obj):
    #    return obj.reg_date

    def get_form(self, request, obj=None, change=False, **kwargs):
        kwargs['fields'] = flatten_fieldsets(self.fieldsets)
        form = super(UnidadesCriticasAdmin, self).get_form(request, obj, change, **kwargs)

        return form

    def get_fieldsets(self, request, obj=None):
        fieldsets = super(UnidadesCriticasAdmin, self).get_fieldsets(request, obj)
        newfieldsets = list(fieldsets)
        fields = []
        for field in ExtraFieldType.objects.filter(model='UnidadesCriticas'):
            fields.append(field.name)
        if fields:
            newfieldsets.append(['Metadatos', {'fields': fields}])

        return newfieldsets

    def response_change(self, request, obj):
        unidad_critica_id = request.resolver_match.kwargs['object_id']

        if "_save" in request.POST:
            for field in ExtraFieldType.objects.filter(model='UnidadesCriticas'):
                if field.name in request.POST:
                    selected_value = request.POST[field.name]
                    field_id = ExtraFieldType.objects.filter(name=field.name).first().pk
                    extra_field = ExtraField.objects.filter(unidades_criticas=unidad_critica_id).filter(field_type=field_id).first()
                    if extra_field is None : 
                        extra_field = ExtraField(
                            unidades_criticas = UnidadesCriticas.objects.get(pk=unidad_critica_id),
                            field_type = ExtraFieldType.objects.get(pk=field_id),
                            value = selected_value
                        )
                    else : 
                        extra_field.value = selected_value
                    extra_field.save()
        return super().response_change(request, obj)

    def response_add(self, request, obj, post_url_continue=None):
        if "_save" in request.POST:
            for field in ExtraFieldType.objects.filter(model='UnidadesCriticas'):
                if field.name in request.POST:
                    selected_value = request.POST[field.name]
                    field_id = ExtraFieldType.objects.filter(name=field.name).first().pk
                    extra_field = ExtraField.objects.filter(unidades_criticas=obj.id).filter(field_type=field_id).first()
                    if extra_field is None : 
                        extra_field = ExtraField(
                            unidades_criticas = UnidadesCriticas.objects.get(pk=obj.id),
                            field_type = ExtraFieldType.objects.get(pk=field_id),
                            value = selected_value
                        )
                    else : 
                        extra_field.value = selected_value
                    extra_field.save()
        return super().response_add(request, obj, post_url_continue= post_url_continue)



admin.site.register(Profesion)
admin.site.register(Especialidad)
admin.site.register(Dependencia)
admin.site.register(TipoInstalacion)
admin.site.register(Nivel)
admin.site.register(Instalacion, InstalacionAdmin)
admin.site.register(Servicio, ServicioAdmin)
admin.site.register(Employee, EmployeeAdmin)
admin.site.register(Position, PositionAdmin)
admin.site.register(ExtraFieldType, ExtraFieldTypeAdmin)
admin.site.register(UnidadesCriticas, UnidadesCriticasAdmin)