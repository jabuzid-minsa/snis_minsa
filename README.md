# Sistema Nacional de Inteligencia en Salud del MINSA

Documentación Técnica del Sistema

## Configuración Web Service

Instalar via *pip* el servicio web de Django. 
```
pip install djangorestframework
```

Agregar 'rest_framework' en la seccion INSTALLED_APPS de setting.py y la autenticación.

```python

INSTALLED_APPS = [
    ...
    'rest_framework',
    'rest_framework.authtoken',
]

REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework.authentication.TokenAuthentication',
    ],
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
    'PAGE_SIZE': 100
}
```

En el archivo *rest_api/views.py* se asignan los permisos de accesos a la información a través de un ViewSet. 
Tambien se hace el link con la clase serializadora que se encarga de devolver la información. Ejemplo del ViewSet

```python
class InstalacionViewSet(viewsets.ModelViewSet):
    permission_classes = (IsAuthenticated,)
    queryset = Instalacion.objects.all().order_by('id')
    serializer_class = InstalacionSerializer
```

Por cada tabla (modelo) de la aplicación se podrá extraer la información necesaria. En el archivo *rest_api/serializers.py*
se creará un Serializer por cada servicio. Por ejemplo, para el modelo *Instalacion* se creará una clase serializadora 
InstalacionSerializer con los respectivos campos que seran devueltos. A continuación se muestra la clase que devuelve la información 
en formato JSON:

```python
class InstalacionSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    instalacion = serializers.CharField()
    cod_inst = serializers.CharField()
    tipo_instalacion = serializers.StringRelatedField()
    nivel = serializers.StringRelatedField()
    latitude = serializers.DecimalField(max_digits=9, decimal_places=6)
    longitude = serializers.DecimalField(max_digits=9, decimal_places=6)
    corregimiento = serializers.StringRelatedField()
    dependencia = serializers.StringRelatedField()
    region_dependencia = serializers.StringRelatedField()
    servicios = serializers.StringRelatedField(many=True)

    class Meta:
        model = Instalacion
```

Para el redireccionamiento url se usa el archivo *rest_api/urls.py*, en el siguiente caso se asigna al url la terminacion *instalaciones*
y se contacta el ViewSet.

```python
router = routers.DefaultRouter()
router.register(r'instalaciones', views.InstalacionViewSet)
```
