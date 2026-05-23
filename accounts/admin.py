from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User


@admin.register(User)
class CustomUserAdmin(UserAdmin):
    list_display  = ('username', 'email', 'rol', 'is_staff', 'is_active')
    list_filter   = ('rol', 'is_staff', 'is_active')
    list_editable = ('rol',)   # edita el rol directamente en la lista sin entrar al detalle

    # Mueve el campo 'rol' al primer fieldset (Datos personales) para que sea lo primero que se vea
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        ('Rol en el sistema', {'fields': ('rol',), 'classes': ('wide',)}),
        ('Datos personales',  {'fields': ('first_name', 'last_name', 'email')}),
        ('Permisos',          {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        ('Fechas',            {'fields': ('last_login', 'date_joined'), 'classes': ('collapse',)}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'rol', 'password1', 'password2'),
        }),
    )