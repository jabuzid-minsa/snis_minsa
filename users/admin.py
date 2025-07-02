from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin

from .forms import CustomUserCreationForm, CustomUserChangeForm
from .models import CustomUser

class CustomUserAdmin(UserAdmin):
    add_form = CustomUserCreationForm
    form = CustomUserChangeForm
    model = CustomUser
    list_display = ['username', 'first_name', 'last_name', 'email','is_staff' ]
    #autocomplete_fields = ['region', 'instalacion']

    fieldsets = (
        ((''), {'fields': ('username','password')}),
        (('Información personal'), {'fields': ('first_name', 'last_name', 'email')}),
        (('Permisos'), {'fields': ('is_active', 'is_staff', 'is_superuser','role', 'instalaciones', 'groups', 'user_permissions',)}),
        (('Fechas importantes'), {'fields': ('last_login', 'date_joined')}),
    )

    filter_horizontal = ('instalaciones','groups','user_permissions')

admin.site.register(CustomUser, CustomUserAdmin)