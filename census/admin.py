from django.contrib import admin
from .models import Population

class PopulationAdmin(admin.ModelAdmin):
    raw_id_fields = ['contra_key']
    #autocomplete_fields = ['contra_key']
    list_display = ('contra_key', 'residences', 'non_indigenous' , 'indigenous')
    search_fields = ('contra_key__poblado', )

admin.site.register(Population, PopulationAdmin)
