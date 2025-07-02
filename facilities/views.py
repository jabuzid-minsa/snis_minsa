from django.views import generic
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import FormMixin
from .models import UnidadesCriticas, Instalacion
from .forms import UnidadesCriticasForm, UCFilterForm
from political_division.models import Provincia, Distrito, Corregimiento
from users.models import CustomUser
from django.core import serializers
from django.http import HttpResponse
from django.urls import reverse_lazy
from django.contrib.auth.decorators import login_required, permission_required
from django.utils.decorators import method_decorator
from django.urls import reverse
from django.http import HttpResponseRedirect
from datetime import datetime
from django.db.models import Q
from django.http import JsonResponse
from dal import autocomplete
import xlwt

class IndexView(generic.TemplateView):
    template_name = 'facilities/index.html'

    @method_decorator(login_required)
    @method_decorator(permission_required('facilities.view_unidadescriticas'))
    def dispatch(self, *args, **kwargs):
        return super(IndexView, self).dispatch(*args, **kwargs)

class UnidadesCriticasCreate(CreateView):
    model = UnidadesCriticas
    form_class = UnidadesCriticasForm

    def get_success_url(self):
          return reverse_lazy('facilities:uc-detail', kwargs={'pk': self.object.id })

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['create'] = True
        return context

    def get_form_kwargs(self):
        kwargs = super(UnidadesCriticasCreate, self).get_form_kwargs()
        kwargs['user'] = self.request.user
        pref = {'reg_date': datetime.today().strftime('%Y-%m-%d %H:%M:%S')}
        
        if self.request.user.instalaciones.all().count() == 1:
            instalacion = self.request.user.instalaciones.first()
            pref.update( {'instalacion': instalacion} )
       
        kwargs.update(initial = pref)

        return kwargs

    def get_form(self ,form_class=None):
        form = super().get_form(form_class=self.form_class)
        form.fields['instalacion'].queryset = self.request.user.instalaciones.all()
        return form
        
    @method_decorator(login_required)
    @method_decorator(permission_required('facilities.add_unidadescriticas'))
    def dispatch(self, *args, **kwargs):
        return super(UnidadesCriticasCreate, self).dispatch(*args, **kwargs)

class UnidadesCriticasDetail(DetailView):
    model = UnidadesCriticas
    context_object_name = 'uc'

    @method_decorator(login_required)
    @method_decorator(permission_required('facilities.view_unidadescriticas'))
    def dispatch(self, *args, **kwargs):
        return super(UnidadesCriticasDetail, self).dispatch(*args, **kwargs)

class UnidadesCriticasUpdate(UpdateView):
    model = UnidadesCriticas
    form_class = UnidadesCriticasForm
    
    def get_success_url(self):
          return reverse_lazy('facilities:uc-detail', kwargs={'pk': self.object.id })

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['approved'] = context['object'].aprobado
        context['create'] = False
        return context
    
    def get_form_kwargs(self):
        kwargs = super(UnidadesCriticasUpdate, self).get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs

    def get_form(self ,form_class=None):
        form = super().get_form(form_class=self.form_class)
        form.fields['instalacion'].queryset = self.request.user.instalaciones.all()
        if self.object.aprobado:
            form.fields['aprobado'].disabled = True
        return form

    @method_decorator(login_required)
    @method_decorator(permission_required('facilities.change_unidadescriticas'))
    def dispatch(self, *args, **kwargs):
        return super(UnidadesCriticasUpdate, self).dispatch(*args, **kwargs)

class UnidadesCriticasDelete(DeleteView):
    model = UnidadesCriticas
    success_url = reverse_lazy('facilities:index')

    @method_decorator(login_required)
    @method_decorator(permission_required('facilities.delete_unidadescriticas'))
    def dispatch(self, *args, **kwargs):
        return super(UnidadesCriticasDelete, self).dispatch(*args, **kwargs)

class UnidadesCriticasListView(FormMixin, ListView):
    model = UnidadesCriticas
    paginate_by = 50
    context_object_name = 'ucl'
    form_class = UCFilterForm
    queryset = None 

    #def post(self, request):
    #    self.object_list = self.get_queryset() 
    #    return HttpResponseRedirect(reverse('facilities:uc-list'))

    def get_form(self ,form_class=None):
        form = super().get_form(form_class=self.form_class)
        form.fields['instalacion'].queryset = self.request.user.instalaciones.all()

        instalacion = self.request.GET.get('instalacion')
        reg_date = self.request.GET.get('reg_date')
        status = self.request.GET.get('status')

        if instalacion:
            form.initial['instalacion'] = instalacion
        if reg_date:
            form.initial['reg_date'] = reg_date
        if status:
            form.initial['status'] = status
        return form

    def get_queryset(self):
        instalacion = self.request.GET.get('instalacion')
        reg_date = self.request.GET.get('reg_date')
        status = self.request.GET.get('status')

        x = Q()
        for inst in self.request.user.instalaciones.all():
            x = x | Q (instalacion = inst)

        
        uc_filtered = super().get_queryset().filter(x)

        #temp patch
        uc_filtered = uc_filtered.exclude(camas_sala = None, camas_otro_sala = None, vent_dispo=None)
        
         #self.publisher = 'd'#get_object_or_404(UnidadesCriticas, name=self.kwargs['publisher'])
        if instalacion:
            uc_filtered = uc_filtered.filter(instalacion = instalacion)
        if reg_date:
            form_date = datetime.strptime(reg_date, '%Y-%m-%d').date()
            uc_filtered = uc_filtered.filter(reg_date__date = form_date)
        if status == '2':
            uc_filtered = uc_filtered.filter(aprobado=True)
        elif status == '3': 
            uc_filtered = uc_filtered.filter(aprobado=False)

        return uc_filtered.order_by('-reg_date') 

    @method_decorator(login_required)
    @method_decorator(permission_required('facilities.view_unidadescriticas'))
    def dispatch(self, *args, **kwargs):
        return super(UnidadesCriticasListView, self).dispatch(*args, **kwargs)
    
    class Meta:
        ordering = ['-reg_date']

class InstalacionAutocomplete(autocomplete.Select2QuerySetView):
    def get_queryset(self):
        qs = self.request.user.instalaciones.all()

        if self.q:
            qs = qs.filter(instalacion__icontains=self.q)

        return qs

def load_distritos(request):
    provincia_id = request.GET.get('provincia')
    distritos = Distrito.objects.filter(provincia = provincia_id)
    data = serializers.serialize("json", distritos)
    return HttpResponse(data, content_type='application/json')

def load_corregimientos(request):
    distrito_id = request.GET.get('distrito')
    corregimientos = Corregimiento.objects.filter(distrito = distrito_id)
    data = serializers.serialize("json", corregimientos)
    return HttpResponse(data, content_type='application/json')

def load_instalacion_by_corregimiento(request):
    corregimiento_id = request.GET.get('corregimiento')
    instalaciones = Instalacion.objects.filter(corregimiento = corregimiento_id)
    data = serializers.serialize("json", instalaciones)
    return HttpResponse(data, content_type='application/json')


def approve_report(request):
    uc_id = request.GET.get('id')
    try:
        uc = UnidadesCriticas.objects.get(id = uc_id)
        uc.aprobado = not uc.aprobado
        uc.save()
        data = {'status':'valid'}
    except:
        data = {'error': True}

    return JsonResponse(data)

def export_xls(request):
    id_instalacion = request.GET.get('id_instalacion')
    reg_date = request.GET.get('reg_date')
    status = request.GET.get('id_status')
    
    response = HttpResponse(content_type='application/ms-excel')
    response['Content-Disposition'] = 'attachment; filename="reportes-covid.xls"'
    
    wb = xlwt.Workbook(encoding='utf-8')
    ws = wb.add_sheet('Reportes')

    row_num = 0

    font_style = xlwt.XFStyle()
    font_style.font.bold = True

    columns = ['Instalacion', 
            'Fecha', 
            'Camas UCI', 
            'Camas Semi Intensivos',
            'Camas en sala',
            'Camas ocupadas por COVID-19',
            'Camas COVID-19 en sala',
            'Camas otras causas',
            'Camas otras causas en sala',
            'Ventiladores disponibles',
            'Transporte',
            'Fijo',

            'Pacientes con COVID-19 con VMA en UCI',
            'Transporte',
            'Fijo',

            'Pacientes con COVID-19 con VMA en Semi-intensivos',
            'Transporte',
            'Fijo',

            'Pacientes con COVID-19 con VMA en sala',
            'Transporte',
            'Fijo',
            'Ventiladores ocupados con otras patologías',
            'Transporte',
            'Fijo',
            'Pacientes con COVID-19 con intubacion',
            'Pacientes con COVID-19 que fueron extubados',
            'Pacientes trasladados de UCI a sala',
            'Defunciones por COVID-19',
            'Observaciones',
            'Médicos Intensivistas Totales',
            'Disponibles',
            'Médicos Internistas Totales',
            'Disponibles',
            'Médicos Infectólogo',
            'Disponibles',
            'Médicos Anestesiólogos Totales',
            'Disponibles',
            'Médicos Neumólogos Totales',
            'Disponibles',
            'Médicos Cirujanos',
            'Disponibles',
            'Enfermeros Totales',
            'Disponibles',
            'Técnicos/Auxiliares Enfermería Totales',
            'Disponibles',
            'Terapistas Respiratorios',
            'Disponibles',
            'Observaciones']

    for col_num in range(len(columns)):
        ws.write(row_num, col_num, columns[col_num], font_style)

    # Sheet body, remaining rows
    font_style = xlwt.XFStyle()

    if not id_instalacion:
        rows = UnidadesCriticas.objects.all()
    else:
        rows = UnidadesCriticas.objects.filter(instalacion=id_instalacion)

    if reg_date:
        form_date = datetime.strptime(reg_date, '%Y-%m-%d').date()
        rows = rows.filter(reg_date__date = reg_date)

    if status == '2':
        rows = rows.filter(aprobado=True)
    elif status == '3': 
        rows = rows.filter(aprobado=False)

    #patch remove
    rows = rows.exclude(camas_sala = None, camas_otro_sala = None, vent_dispo=None)

    data = ['instalacion', 
            'reg_date', 
            'camas_uci', 
            'camas_semi',
            'camas_sala',
            'camas_covid',
            'camas_covid_sala',
            'camas_otro',
            'camas_otro_sala',

            'vent_dispo',
            'vent_dispo_trans',
            'vent_dispo_fijo',

            'pacientes_vma', 
            'pacientes_vma_trans', 
            'pacientes_vma_fijo', 

            'pacientes_vma_semi',
            'pacientes_vma_semi_trans',
            'pacientes_vma_semi_fijo',

            'pacientes_vma_sala', 
            'pacientes_vma_sala_trans',
            'pacientes_vma_sala_fijo',

            'vent_otro',
            'vent_otro_trans',
            'vent_otro_fijo',

            'pacientes_covid_int',
            'pacientes_covid_ext',
            'pacientes_traslado',
            'defunciones_covid',
            'observaciones_camas',
            'intensivistas',
            'intensivistas_dispo',
            'internistas', 
            'internistas_dispo',
            'infectologos',
            'infectologos_dispo',
            'anestesiologos',
            'anestesiologos_dispo', 
            'neumologos',
            'neumologos_dispo', 
            'cirujanos',
            'cirujanos_dispo',
            'enfermeros',
            'enfermeros_dispo',
            'tecnicos',
            'tecnicos_dispo', 
            'terapistas_resp',
            'terapistas_resp_dispo',
            'observaciones_rh']

    for row in rows:
        row_num += 1
        for col_num in range(len(data)):
            if data[col_num] == 'instalacion':
                value = row.instalacion.instalacion
            elif data[col_num] == 'reg_date':
                value = row.reg_date.strftime('%d-%m-%Y')
            else:
                value = getattr(row, data[col_num])
            ws.write(row_num, col_num, value , font_style)
    
    wb.save(response)
    return response

