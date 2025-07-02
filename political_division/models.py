from django.db import models

class Provincia(models.Model):
    provincia = models.CharField(max_length=150)
    cod_prov = models.CharField("Código", null=True, blank=True, max_length=2, unique=True)
    poligono_id = models.PositiveIntegerField("Polígono Id", null=True, blank=True, unique=True)
    
    def __str__(self):
        return self.provincia

    class Meta:
        verbose_name = 'provincia'
        verbose_name_plural = 'provincias'
        ordering = ["provincia",]

class Region(models.Model):
    provincia = models.ForeignKey(Provincia, on_delete=models.CASCADE, verbose_name="Provincia")
    region = models.CharField("Región", max_length=150)
    cod_reg = models.CharField("Código", null=True, blank=True, max_length=4)

    def __str__(self):
        return self.region

    class Meta:
        verbose_name = 'región de salud'
        verbose_name_plural = 'regiones de salud'
        ordering = ["region",]

class Distrito(models.Model):
    region = models.ForeignKey(Region, null=True, on_delete=models.SET_NULL, verbose_name="Región")
    provincia = models.ForeignKey(Provincia, null=True, on_delete=models.SET_NULL, verbose_name="Provincia")
    distrito = models.CharField("Distrito", max_length=150)
    cod_dist = models.CharField("Código", null=True, blank=True, max_length=6)
    poligono_id = models.PositiveIntegerField("Polígono Id", null=True, blank=True, unique=True)

    def __str__(self):
        return self.distrito
    
    class Meta:
        verbose_name = 'distrito'
        verbose_name_plural = 'distritos'
        ordering = ["distrito",]

class Corregimiento(models.Model):
    distrito = models.ForeignKey(Distrito, on_delete=models.CASCADE, verbose_name="Distrito")
    corregimiento = models.CharField("Corregimiento", max_length=150)
    cod_corr = models.CharField("Código", null=True, blank=True, max_length=8)
    poligono_id = models.PositiveIntegerField("Polígono Id", null=True, blank=True, unique=True)

    def get_provincia(self):
        return self.distrito.provincia
    get_provincia.admin_order_field = 'provincia'
    get_provincia.short_description = 'Provincia'

    provincia = property(get_provincia)

    def __str__(self):
        return self.corregimiento

    class Meta:
        verbose_name = 'corregimiento'
        verbose_name_plural = 'corregimientos'
        ordering = ["corregimiento",]

class Poblado(models.Model):
    corregimiento = models.ForeignKey(Corregimiento, on_delete=models.CASCADE, verbose_name="Corregimiento")
    poblado = models.CharField("Poblado", max_length=150)
    cod_pob = models.CharField("Código", null=True, blank=True, max_length=10)
    contra_key = models.CharField("Llave de contraloria", null=True, blank=True, unique=True, max_length=150)

    def get_distrito(self):
        return self.corregimiento.distrito
    get_distrito.admin_order_field = 'distrito'
    get_distrito.short_description = 'Distrito'
    distrito = property(get_distrito)

    def get_provincia(self):
        return self.corregimiento.distrito.provincia
    get_provincia.admin_order_field = 'provincia'
    get_provincia.short_description = 'Provincia'
    provincia = property(get_provincia)

    def __str__(self):
        return self.poblado
    
    class Meta:
        verbose_name = 'poblado'
        verbose_name_plural = 'poblados'
        ordering = ["poblado",]