from .models import UnidadesCriticas, Instalacion
from django.forms import ModelForm
from django import forms
from political_division.models import Provincia, Distrito, Corregimiento
from django.core import validators
from datetime import datetime
from dal import autocomplete
from django.urls import reverse

class UnidadesCriticasForm(ModelForm):

    instalacion = forms.ModelChoiceField(label='Instalación', empty_label='-------', queryset=Instalacion.objects.none(),required=False, widget=autocomplete.ModelSelect2(url='facilities:instalacion-autocomplete',attrs={
        'data-placeholder': 'Instalación...',
        'data-minimum-input-length': 3,
        'id':'instalacion'
        },) )
    reg_date = forms.DateTimeField(input_formats=['%Y-%m-%d %H:%M:%S'],label="Fecha de registro",widget=forms.TextInput(attrs={'class':'form-control datetimepicker',}), required=True)
    aprobado = forms.BooleanField(label="Aprobado",required=False)

    camas_uci = forms.IntegerField(label="1. Camas UCI",help_text='Total de camas UCI que tiene el hospital (estén o no ocupadas).', min_value=0, widget=forms.TextInput(attrs={'class':'form-control'}), required=False)
    camas_semi= forms.IntegerField(label="2. Camas Semi Intensivos",help_text='Total de camas semi-intensivos que tiene el hospital (estén o no ocupadas).', min_value=0, widget=forms.TextInput(attrs={'class':'form-control'}),required=False)
    camas_sala = forms.IntegerField(label = "3. Camas en sala",help_text='Total de camas en sala (no incluir camas de UCI o semi-intensivo, estén o no ocupadas).', min_value=0, widget=forms.TextInput(attrs={'class':'form-control'}),required=False)
    camas_covid= forms.IntegerField(label="4. Camas ocupadas por COVID-19",help_text='Camas ocupadas por pacientes con COVID-19 en UCI o semi intensivo (incluir casos sospechosos y confirmados).',  min_value=0, widget=forms.TextInput(attrs={'class':'form-control'}),required=False)
    camas_covid_sala = forms.IntegerField(label="5. Camas COVID-19 en sala", help_text='Camas ocupadas por pacientes con COVID-19 en sala (incluir sospechosos y confirmados; no incluir camas de UCI o semiintensivo).', min_value=0, widget=forms.TextInput(attrs={'class':'form-control'}),required=False)
    camas_otro= forms.IntegerField(label="6. Camas otras causas",help_text='Camas ocupadas por otras causas de UCI y Semi-intensivo',  min_value=0, widget=forms.TextInput(attrs={'class':'form-control'}),required=False)
    camas_otro_sala = forms.IntegerField(label="7. Camas otras causas en sala",help_text='Camas ocupadas por otras causas en sala (no incluir camas de UCI o semi-intensivo).', min_value=0, widget=forms.TextInput(attrs={'class':'form-control'}),required=False)
    
    vent_dispo= forms.IntegerField(label="8. Ventiladores disponibles",help_text='Total de ventiladores que tiene el hospital (estén o no ocupados). Sumar ventiladores de transporte, no invasivos y estacionarios.', min_value=0, widget=forms.TextInput(attrs={'class':'form-control'}),required=False)
    vent_dispo_trans= forms.IntegerField(label="Transporte", min_value=0, widget=forms.TextInput(attrs={'class':'form-control'}),required=False)
    vent_dispo_fijo= forms.IntegerField(label="Fijo",min_value=0, widget=forms.TextInput(attrs={'class':'form-control'}),required=False)

    pacientes_vma= forms.IntegerField(label="9. Pacientes con COVID-19 con VMA en UCI",help_text='Pacientes sospechosos y confirmados con COVID-19 con VMA en UCI.', min_value=0, widget=forms.TextInput(attrs={'class':'form-control'}),required=False)
    pacientes_vma_trans= forms.IntegerField(label="Transporte", min_value=0, widget=forms.TextInput(attrs={'class':'form-control'}),required=False)
    pacientes_vma_fijo= forms.IntegerField(label="Fijo",min_value=0, widget=forms.TextInput(attrs={'class':'form-control'}),required=False)

    pacientes_vma_semi= forms.IntegerField(label="10. Pacientes con COVID-19 con VMA en Semi-intensivos",help_text='Pacientes sospechosos y confirmados con COVID-19 con VMA en Semi-intensivos.', min_value=0, widget=forms.TextInput(attrs={'class':'form-control'}),required=False)
    pacientes_vma_semi_trans= forms.IntegerField(label="Transporte", min_value=0, widget=forms.TextInput(attrs={'class':'form-control'}),required=False)
    pacientes_vma_semi_fijo= forms.IntegerField(label="Fijo",min_value=0, widget=forms.TextInput(attrs={'class':'form-control'}),required=False)

    pacientes_vma_sala = forms.IntegerField(label="11. Pacientes con COVID-19 con VMA en sala",help_text='Pacientes sospechosos y confirmados con COVID-19 con VMA en Sala.', min_value=0, widget=forms.TextInput(attrs={'class':'form-control'}),required=False)
    pacientes_vma_sala_trans= forms.IntegerField(label="Transporte", min_value=0, widget=forms.TextInput(attrs={'class':'form-control'}),required=False)
    pacientes_vma_sala_fijo= forms.IntegerField(label="Fijo",min_value=0, widget=forms.TextInput(attrs={'class':'form-control'}),required=False)

    vent_otro= forms.IntegerField(label="12. Ventiladores ocupados con otras patologías",help_text='Número de ventiladores ocupados con otras patologías en este momento.', min_value=0, widget=forms.TextInput(attrs={'class':'form-control'}),required=False)
    vent_otro_trans= forms.IntegerField(label="Transporte", min_value=0, widget=forms.TextInput(attrs={'class':'form-control'}),required=False)
    vent_otro_fijo= forms.IntegerField(label="Fijo",min_value=0, widget=forms.TextInput(attrs={'class':'form-control'}),required=False)

    pacientes_covid_int= forms.IntegerField(label="13. Pacientes con COVID-19 con intubacion",help_text='Pacientes sospechosos y confirmados COVID-19 con intubacion (sumar Intensivo y Semi Intensivo y sala).', min_value=0, widget=forms.TextInput(attrs={'class':'form-control'}),required=False)
    pacientes_covid_ext= forms.IntegerField(label="14. Pacientes con COVID-19 que fueron extubados",help_text='Pacientes sospechosos y confirmados COVID-19 que fueron extubados el día de hoy.', min_value=0, widget=forms.TextInput(attrs={'class':'form-control'}),required=False)
    pacientes_traslado= forms.IntegerField(label="15. Pacientes trasladados de UCI a sala",help_text='Pacientes  sospechosos y confirmados COVID-19 que fueron trasladados de UCI a sala el día de hoy.', min_value=0, widget=forms.TextInput(attrs={'class':'form-control'}),required=False)
    defunciones_covid= forms.IntegerField(label="16. Defunciones por COVID-19",help_text='Defunciones por COVID-19 el día de hoy (sumar sospechosos y confirmados).', min_value=0, widget=forms.TextInput(attrs={'class':'form-control'}),required=False)
    observaciones_camas = forms.CharField(label = "17. Observaciones", required=False, widget= forms.Textarea(attrs={'rows':8, 'cols':100, 'class':'form-control'}))
    intensivistas= forms.IntegerField(label="18. Intensivistas Totales", min_value=0, widget=forms.TextInput(attrs={'class':'form-control'}),required=False)
    intensivistas_dispo= forms.IntegerField(label="Disponibles", min_value=0, widget=forms.TextInput(attrs={'class':'form-control'}),required=False)
    internistas= forms.IntegerField(label="19. Internistas Totales", min_value=0, widget=forms.TextInput(attrs={'class':'form-control'}),required=False)
    internistas_dispo= forms.IntegerField(label="Disponibles", min_value=0, widget=forms.TextInput(attrs={'class':'form-control'}),required=False)
    infectologos= forms.IntegerField(label="20. Infectólogo Totales", min_value=0, widget=forms.TextInput(attrs={'class':'form-control'}),required=False)
    infectologos_dispo= forms.IntegerField(label="Disponibles", min_value=0, widget=forms.TextInput(attrs={'class':'form-control'}),required=False)
    anestesiologos= forms.IntegerField(label="21. Anestesiólogos Totales", min_value=0, widget=forms.TextInput(attrs={'class':'form-control'}),required=False)
    anestesiologos_dispo= forms.IntegerField(label="Disponibles", min_value=0, widget=forms.TextInput(attrs={'class':'form-control'}),required=False)
    neumologos= forms.IntegerField(label="22. Neumólogos Totales", min_value=0, widget=forms.TextInput(attrs={'class':'form-control'}),required=False)
    neumologos_dispo= forms.IntegerField(label="Disponibles", min_value=0, widget=forms.TextInput(attrs={'class':'form-control'}),required=False)
    cirujanos = forms.IntegerField(label="23. Cirujanos Totales", min_value=0, widget=forms.TextInput(attrs={'class':'form-control'}),required=False)
    cirujanos_dispo = forms.IntegerField(label="Disponibles", min_value=0, widget=forms.TextInput(attrs={'class':'form-control'}),required=False)
    enfermeros= forms.IntegerField(label="24. Enfermeros Totales", min_value=0, widget=forms.TextInput(attrs={'class':'form-control'}),required=False)
    enfermeros_dispo= forms.IntegerField(label="Disponibles",widget=forms.TextInput(attrs={'class':'form-control'}),required=False)
    tecnicos= forms.IntegerField(label="25. Técnicos/Auxiliares Enfermería Totales", min_value=0, widget=forms.TextInput(attrs={'class':'form-control'}),required=False)
    tecnicos_dispo= forms.IntegerField(label="Disponibles", min_value=0, widget=forms.TextInput(attrs={'class':'form-control'}),required=False)
    terapistas_resp = forms.IntegerField(label="26. Terapistas Respiratorios", min_value=0, widget=forms.TextInput(attrs={'class':'form-control'}),required=False)
    terapistas_resp_dispo = forms.IntegerField(label="Disponibles", min_value=0, widget=forms.TextInput(attrs={'class':'form-control'}),required=False)
    observaciones_rh = forms.CharField(label = "27. Observaciones", required=False, widget= forms.Textarea(attrs={'rows':8, 'cols':100, 'class':'form-control'}))

    def __init__(self, user, *args, **kwargs):
        super(UnidadesCriticasForm, self).__init__(*args, **kwargs)
        instance = getattr(self, 'instance', None)
        if (instance and instance.pk and instance.aprobado is True) and (not user.is_superuser) :
            for key,field in self.fields.items():
                field.disabled = True

    def is_valid(self):
        ret = forms.Form.is_valid(self)
        for f in self.errors:
            self.fields[f].widget.attrs.update({'class': self.fields[f].widget.attrs.get('class', '') + ' is-invalid'})
        return ret

    class Meta:
        model = UnidadesCriticas
        fields = ('__all__')


class UCFilterForm(forms.Form):
    CHOICES = (
        (1, 'Aprobados/No Aprobados'),
        (2, 'Aprobados'),
        (3, 'No Aprobados'),
    )
    instalacion = forms.ModelChoiceField(label='Instalación', empty_label='-------', queryset=Instalacion.objects.none(),required=False, widget=autocomplete.ModelSelect2(url='facilities:instalacion-autocomplete',attrs={
        'data-placeholder': 'Instalación...',
        'data-minimum-input-length': 3,
        'id':'instalacion'
        },) )
    reg_date = forms.DateField(input_formats=['%Y-%m-%d'],label="Fecha de registro",widget=forms.TextInput(attrs={'class':'form-control datetimepicker',}),required=False)
    status = forms.ChoiceField(label='Estatus', choices=CHOICES, widget=forms.Select(attrs={'class':'form-control'}))
