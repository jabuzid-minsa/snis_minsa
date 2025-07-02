from django.db import models
from political_division.models import Provincia, Region, Distrito, Corregimiento, Poblado

class Dependencia(models.Model):
    dependencia = models.CharField("Dependencia", max_length=150)
    codigo = models.CharField("Código", max_length=2, unique=True)

    def __str__(self):
        return self.dependencia
    
    class Meta:
        verbose_name = 'dependencia'
        verbose_name_plural = 'dependencias'

class TipoInstalacion(models.Model):
    tipo_instalacion = models.CharField("Tipo de Instalación", max_length=150)
    codigo = models.CharField("Código", max_length=2, unique=True)

    def __str__(self):
        return self.tipo_instalacion
    
    class Meta:
        verbose_name = 'tipo de instalación'
        verbose_name_plural = 'tipos de instalación'
        ordering = ["tipo_instalacion"]

class Nivel(models.Model):
    nivel = models.CharField("Nivel", max_length=150)
    codigo = models.CharField("Código", max_length=2, unique=True)

    def __str__(self):
        return self.nivel
    
    class Meta:
        verbose_name = 'nivel'
        verbose_name_plural = 'niveles'

class Instalacion(models.Model):
    corregimiento = models.ForeignKey(Corregimiento, on_delete=models.CASCADE, verbose_name="Corregimiento")
    dependencia = models.ForeignKey(Dependencia, null=True, on_delete=models.SET_NULL, verbose_name="Dependencia")
    tipo_instalacion = models.ForeignKey(TipoInstalacion, null=True, on_delete=models.SET_NULL, verbose_name="Tipo de Instalación")
    region_dependencia = models.ForeignKey(Region, null=True, blank=True, on_delete=models.SET_NULL, verbose_name="Región Asociada")
    nivel = models.ForeignKey(Nivel, null=True, on_delete=models.SET_NULL, verbose_name="Nivel")
    instalacion = models.CharField("Instalación", max_length=150)
    cod_inst = models.CharField("Código", max_length=13, null=True, blank=True)
    latitude = models.DecimalField("Latitud", null=True, blank=True, max_digits=9, decimal_places=6)
    longitude = models.DecimalField("Longitud", null=True, blank=True, max_digits=9, decimal_places=6)
    servicios = models.ManyToManyField('Servicio', blank=True)
    observaciones = models.TextField("Observaciones", null = True, blank=True)

    def __str__(self):
        return self.instalacion
    
    class Meta:
        verbose_name = 'instalación'
        verbose_name_plural = 'instalaciones'
        ordering = ["instalacion"]

class InstalacionPoblado(models.Model):
    instalacion = models.ForeignKey(Instalacion, on_delete=models.CASCADE)
    poblado = models.ForeignKey(Poblado, on_delete=models.CASCADE)

    class Meta:
        constraints = [models.UniqueConstraint(fields=['instalacion', 'poblado'], name='unique_instalacion_poblado')]

class Servicio(models.Model):
    servicio = models.CharField("Servicio", max_length=150)
    codigo = models.CharField("Código", max_length=2, unique=True)
    
    class Meta:
        ordering = ('servicio',)
    
    def __str__(self):
        return self.servicio

class Horario(models.Model):
    horario = models.CharField("Horario", max_length=150)
    opening_time = models.TimeField("Inicio", blank=False)
    closing_time = models.TimeField("Fin", blank=False)
    instalacion = models.ForeignKey(Instalacion, on_delete=models.CASCADE, verbose_name="Instalación")

    def __str__(self):
        return self.horario

class Position(models.Model):
    position = models.CharField("Cargo", max_length=150)

    class Meta:
        verbose_name = 'cargo'
        verbose_name_plural = 'cargos'
        ordering = ["position",]

    def __str__(self):
        return self.position

class Employee(models.Model):
    PERM = 1
    TRANS_INVER = 2
    TRANS = 3
    STATUS = (
        (PERM, 'PERMANENTE'),
        (TRANS_INVER, 'PERS TRANS DE INVERS'),
        (TRANS, 'PERS TRANSITORIO'),
    )

    id_minsa = models.CharField("Identificador Institucional", max_length=5, unique=False, blank=True, null=True)
    name = models.CharField("Nombre", max_length=50)
    last_name = models.CharField("Apellido", max_length=50)
    identity_card = models.CharField("Cédula", max_length=13, blank=True, null=True)
    job_position = models.ForeignKey(Position, blank=True, null=True, on_delete=models.SET_NULL, verbose_name="Cargo")
    salary = models.DecimalField("Salario Mensual", max_digits=6, decimal_places=2, blank=True, null=True)
    start_date = models.DateField("Inicio de labores", blank=True, null=True)
    spend_object = models.CharField("Objeto de gasto", max_length=3, blank=True, null=True)
    status = models.IntegerField("Estatus", choices=STATUS, blank=True, null=True)
    instalaciones = models.ManyToManyField('Instalacion', blank=True)
    especialidades = models.ManyToManyField('Especialidad',blank=True)
    observaciones = models.TextField("Observaciones", null = True, blank=True)

    class Meta:
        verbose_name = 'funcionario'
        verbose_name_plural = 'funcionarios'
        ordering = ["name", "last_name"]
    
    def __str__(self):
        return self.name + ' ' + self.last_name

class Phone(models.Model):
    PHONE = 1
    CEL = 2
    FAX = 3
    PHONE_CHOICES = (
        (PHONE, 'Teléfono'),
        (CEL, 'Celular'),
        (FAX, 'Fax'),
    )
    instalacion = models.ForeignKey(Instalacion, blank=True, null=True, on_delete=models.CASCADE, verbose_name="Instalación")
    employee = models.ForeignKey(Employee, blank=True, null=True, on_delete=models.CASCADE, verbose_name="Funcionario")
    number = models.CharField("Número", max_length=150)
    phone_choise = models.IntegerField("Tipo", choices=PHONE_CHOICES, default=PHONE)

    class Meta:
        verbose_name = 'contacto'
        verbose_name_plural = 'contactos'
    
    def __str__(self):
        return ''

class UnidadesCriticas(models.Model):
    instalacion = models.ForeignKey(Instalacion, on_delete=models.CASCADE, verbose_name="Instalación")
    reg_date = models.DateTimeField("Fecha de registro", null=False,)
    aprobado = models.BooleanField("Aprobado",default=False)

    camas_uci = models.IntegerField("Camas UCI", null=True, blank=True, help_text='Total de camas UCI disponibles en el hospital (estén o no ocupadas)')
    camas_semi = models.IntegerField("Camas Semi Intensivos", null=True, blank=True, help_text='Total de camas en cuidados semi intensivos disponibles (estén o no ocupadas)')
    camas_sala = models.IntegerField("Camas en sala", null=True, blank=True, help_text='Total de camas en sala (no incluir camas de UCI o semiintensivo, estén o no ocupadas)')
    camas_covid = models.IntegerField("Camas ocupadas por COVID-19", null=True, blank=True, help_text='Camas ocupadas con pacientes COVID-19 sospechosos y confirmados internados en intensivo y semi intensivo')
    camas_covid_sala = models.IntegerField("Camas COVID-19 en sala", null=True, blank=True, help_text='Camas ocupadas por pacientes con COVID-19 en sala (incluir sospechosos y confirmados; no incluir camas de UCI o semiintensivo)')
    camas_otro = models.IntegerField("Camas otras causas", null=True, blank=True, help_text='Camas ocupadas con pacientes con otras patologías')
    camas_otro_sala = models.IntegerField("Camas otras causas en sala", null=True, blank=True, help_text='Camas ocupadas por otras causas en sala (no incluir camas de UCI o semiintensivo)')
    

    vent_dispo = models.IntegerField("Ventiladores disponibles", null=True, blank=True, help_text='Total de ventiladores que tiene el hospital (estén o no ocupados) Sumar ventiladores de transporte y estacionarios')
    vent_dispo_trans = models.IntegerField("Ventilador tipo trasporte", null=True, blank=True,)
    vent_dispo_fijo = models.IntegerField("Ventilador tipo fijo", null=True, blank=True,)

    pacientes_vma = models.IntegerField("Pacientes con COVID-19 con VMA en UCI", null=True, blank=True, help_text='Total pacientes COVID-19 sospechosos y confirmados con ventilación mecánica asistida en UCI')
    pacientes_vma_trans = models.IntegerField("Ventilador tipo trasporte", null=True, blank=True,)
    pacientes_vma_fijo = models.IntegerField("Ventilador tipo fijo", null=True, blank=True,)

    pacientes_vma_semi = models.IntegerField("Pacientes con COVID-19 con VMA en Semi-intensivo", null=True, blank=True, help_text='Total pacientes COVID-19 sospechosos y confirmados con ventilación mecánica asistida en Semi-intensivo')
    pacientes_vma_semi_trans = models.IntegerField("Ventilador tipo trasporte", null=True, blank=True,)
    pacientes_vma_semi_fijo = models.IntegerField("Ventilador tipo fijo", null=True, blank=True, )

    pacientes_vma_sala = models.IntegerField("Pacientes con COVID-19 con VMA en sala", null=True, blank=True, help_text='Pacientes sospechosos y confirmados con COVID-19 con VMA en sala (no incluir intensivo ni semi intensivo).')
    pacientes_vma_sala_trans = models.IntegerField("Ventilador tipo trasporte", null=True, blank=True,)
    pacientes_vma_sala_fijo = models.IntegerField("Ventilador tipo fijo", null=True, blank=True,)

    vent_otro = models.IntegerField("Ventiladores ocupados con otras patologías", null=True, blank=True, help_text='Total de ventiladores para pacientes con otras patologías')
    vent_otro_trans = models.IntegerField("Ventilador tipo trasporte", null=True, blank=True,)
    vent_otro_fijo = models.IntegerField("Ventilador tipo fijo", null=True, blank=True,)


    pacientes_covid_int = models.IntegerField("Pacientes con COVID-19 con intubacion", null=True, blank=True, help_text='Total pacientes COVID-19 sospechosos y confirmados con intubacion')
    pacientes_covid_ext = models.IntegerField("Pacientes con COVID-19 que fueron extubados", null=True, blank=True, help_text='Pacientes con COVID-19 que fueron extubados')
    pacientes_traslado = models.IntegerField("Pacientes trasladados de UCI a sala", null=True, blank=True, help_text='Pacientes trasladados de UCI a sala')
    defunciones_covid = models.IntegerField("Defunciones por COVID-19", null=True, blank=True, help_text='Total defunciones por COVID-19 (sospechoso y confirmado)')
    observaciones_camas = models.TextField("Observaciones", null = True, blank=True)

    intensivistas = models.IntegerField("Médicos Intensivistas Totales", null=True, blank=True, )
    internistas = models.IntegerField("Médicos Internistas Totales", null=True, blank=True, )
    infectologos = models.IntegerField("Médicos Infectólogo", null=True, blank=True, )
    anestesiologos = models.IntegerField("Médicos Anestesiólogos Totales", null=True, blank=True, )
    neumologos = models.IntegerField("Médicos Neumólogos Totales", null=True, blank=True, )
    cirujanos = models.IntegerField("Médicos Cirujanos", null=True, blank=True, )
    enfermeros = models.IntegerField("Enfermeros Totales", null=True, blank=True, )
    tecnicos = models.IntegerField("Técnicos/Auxiliares Enfermería Totales", null=True, blank=True, )
    terapistas_resp = models.IntegerField("Terapistas Respiratorios", null=True, blank=True, )
    intensivistas_dispo = models.IntegerField("Disponibles", null=True, blank=True, )
    internistas_dispo = models.IntegerField("Disponibles", null=True, blank=True, )
    infectologos_dispo = models.IntegerField("Disponibles", null=True, blank=True, )
    anestesiologos_dispo = models.IntegerField("Disponibles", null=True, blank=True, )
    neumologos_dispo = models.IntegerField("Disponibles", null=True, blank=True, )
    cirujanos_dispo = models.IntegerField("Disponibles", null=True, blank=True, )
    enfermeros_dispo = models.IntegerField("Disponibles", null=True, blank=True, )
    tecnicos_dispo = models.IntegerField("Disponibles", null=True, blank=True, )
    terapistas_resp_dispo = models.IntegerField("Disponibles", null=True, blank=True, )
    observaciones_rh = models.TextField("Observaciones", null = True, blank=True)


    pacientes_uci = models.IntegerField("Pacientes en UCI COVID-19", null=True, blank=True, help_text='Pacientes COVID-19 sospechosos y confirmados en UCI y SEMI')
    pacientes_uci_otro = models.IntegerField("Pacientes en UCI Otras", null=True, blank=True, help_text='Pacientes con otras patologías en UCI y SEMI')
    ventiladores = models.IntegerField("Pacientes VMA COVID-19", null=True, blank=True, help_text='Pacientes COVID-19 sospechosos y confirmados con ventilación mecánica asistida')
    ventilados_otro = models.IntegerField("Pacientes VMA Otras", null=True, blank=True, help_text='Pacientes con otras patologías con ventilación mecánica asistida')
    intubados = models.IntegerField("Intubados", null=True, blank=True, help_text='Pacientes COVID-19 sospechosos y confirmados intubados')
    extubados = models.IntegerField("Extubados", null=True, blank=True, help_text='Pacientes COVID-19 extubados el día de hoy')
    egresos_uci = models.IntegerField("Trasladados de UCI", null=True, blank=True, help_text='Pacientes sospechosos y confirmados COVID-19 que fueron trasladados de UCI a sala el día de hoy')
    ingresos = models.IntegerField("Ingresos a UCI", null=True, blank=True, help_text='Pacientes sospechosos y confirmados COVID-19 que ingresaron a UCI el día de hoy')
    muertes = models.IntegerField("Defunciones por COVID-19:", null=True, blank=True, help_text='Defunciones por COVID-19 totales (sumar sospechosos y confirmados)')
    observaciones = models.TextField("Observaciones", null = True, blank=True)

    class Meta:
        verbose_name = 'unidad critica'
        verbose_name_plural = 'unidades criticas'

    def get_absolute_url(self):
        from django.urls import reverse
        return reverse('facilities:detail', kwargs={'pk': self.pk})
    
    def __str__(self):
        return "%s   -----------   fecha de registro: %s" % (self.instalacion, str(self.reg_date.strftime("%d/%m/%Y -- %H:%M:%S")))

class ExtraFieldType(models.Model):
    name = models.CharField(max_length=100, verbose_name='Nombre',)
    description = models.CharField(max_length=100, blank=True, null=True, verbose_name='Descripción',)
    model = models.CharField(max_length=40,
        choices=(
            ('Instalacion', 'Instalación'),
            ('Employee', 'Funcionario'),
            ('Provincia', 'Provincia'),
            ('Region', 'Región'),
            ('Distrito', 'Distrito'),
            ('Corregimiento', 'Corregimiento'),
            ('Poblado', 'Poblado'),
            ('UnidadesCriticas', 'Unidades Críticas'),
        ),
        verbose_name='Tabla asociada',
        blank=True, null=True,
    )

    class Meta:
        verbose_name = 'metadato'
        verbose_name_plural = 'metadatos'
        ordering = ['name', ]

    def __str__(self):
        return '{0}'.format(self.name)

class ExtraField(models.Model):
    instalacion = models.ForeignKey(Instalacion, blank=True, null=True, on_delete=models.CASCADE, verbose_name="Instalación")
    employee = models.ForeignKey(Employee, blank=True, null=True, on_delete=models.CASCADE, verbose_name="Funcionario")
    provincia = models.ForeignKey(Provincia, blank=True, null=True, on_delete=models.CASCADE, verbose_name="Provincia")
    region = models.ForeignKey(Region, blank=True, null=True, on_delete=models.CASCADE, verbose_name="Región")
    distrito = models.ForeignKey(Distrito, blank=True, null=True, on_delete=models.CASCADE, verbose_name="Distrito")
    corregimiento = models.ForeignKey(Corregimiento, blank=True, null=True, on_delete=models.CASCADE, verbose_name="Corregimiento")
    poblado = models.ForeignKey(Poblado, blank=True, null=True, on_delete=models.CASCADE, verbose_name="Poblado")
    unidades_criticas = models.ForeignKey(UnidadesCriticas, blank=True, null=True, on_delete=models.CASCADE, verbose_name="Unidades Críticas")

    field_type = models.ForeignKey('ExtraFieldType',verbose_name='Field type',related_name='extra_fields',
        on_delete=models.CASCADE,
        blank=True, null=True,
    )

    value = models.CharField( max_length=200, verbose_name='Value',)

    class Meta:
        ordering = ['field_type__name', ]

    def __str__(self):
        return '{0} ({1}) - {2}'.format(
            self.field_type, self.field_type.get_model_display() or 'general',
            self.value)

class Profesion(models.Model):
    profesion = models.CharField("Profesión", max_length=150)
    codigo = models.CharField("Código", max_length=2, unique=True)

    def __str__(self):
        return self.profesion
    
    class Meta:
        verbose_name = 'profesion'
        verbose_name_plural = 'profesiones'

class Especialidad(models.Model):
    especialidad = models.CharField("Especialidad", max_length=150)
    profesion = models.ForeignKey(Profesion, on_delete=models.CASCADE, verbose_name="Profesión")
    codigo = models.CharField("Código", max_length=2, unique=True)

    def __str__(self):
        return self.especialidad
    
    class Meta:
        verbose_name = 'especialidad'
        verbose_name_plural = 'especialidades'

# Database entity views
class UCEntity(models.Model):
    instalacion_id = models.BigIntegerField(primary_key=True)
    instalacion = models.CharField(max_length=150)
    latitude = models.DecimalField(max_digits=9, decimal_places=6)
    longitude = models.DecimalField(max_digits=9, decimal_places=6)
    region = models.CharField(max_length=150)
    provincia = models.CharField(max_length=150)
    distrito = models.CharField(max_length=150)
    corregimiento = models.CharField(max_length=150)
    dependencia = models.CharField(max_length=150)
    tipo_instalacion = models.CharField(max_length=150)
    nivel = models.CharField(max_length=150)
    director_medico = models.CharField( max_length=200)
    subdirector = models.CharField( max_length=200)
    camas_totales = models.CharField( max_length=200)
    camas_covid19 = models.CharField( max_length=200)
    camas_totales_uci = models.CharField( max_length=200)
    covid19_uci = models.CharField( max_length=200)
    ventiladores_fijos = models.CharField( max_length=200)
    ventiladores_transporte = models.CharField( max_length=200)
    cunas_covid19 = models.CharField( max_length=200)
    carpas_ops = models.CharField( max_length=200)
    contenedores = models.CharField( max_length=200)
    ventiladores = models.CharField( max_length=200)
    camas_ac = models.CharField( max_length=200)
    ventiladores_mecanicos = models.CharField( max_length=200)
    camas_uci_desc = models.CharField( max_length=200)
    camas_semi_desc = models.CharField( max_length=200)
    vent_uso = models.IntegerField()
    ingresos = models.IntegerField()
    egresos_uci = models.IntegerField()
    intubados = models.IntegerField()
    con_ventilador = models.IntegerField()
    muertes = models.IntegerField()
    pacientes_uci = models.IntegerField()
    camas_uci = models.IntegerField()
    camas_semi = models.IntegerField()
    camas_covid = models.IntegerField()
    camas_otro = models.IntegerField()
    vent_dispo = models.IntegerField()
    pacientes_vma = models.IntegerField()
    vent_otro = models.IntegerField()
    pacientes_covid_int = models.IntegerField()
    pacientes_covid_ext = models.IntegerField()
    pacientes_traslado = models.IntegerField()
    defunciones_covid = models.IntegerField()
    intensivistas = models.IntegerField()
    intensivistas_dispo = models.IntegerField()
    internistas = models.IntegerField()
    internistas_dispo = models.IntegerField()
    infectologos = models.IntegerField()
    infectologos_dispo = models.IntegerField()
    anestesiologos = models.IntegerField()
    anestesiologos_dispo = models.IntegerField()
    neumologos = models.IntegerField()
    neumologos_dispo = models.IntegerField()
    enfermeros = models.IntegerField()
    enfermeros_dispo = models.IntegerField()
    tecnicos = models.IntegerField()
    tecnicos_dispo = models.IntegerField()

    class Meta:
        managed = False
        db_table = "uc_entity"