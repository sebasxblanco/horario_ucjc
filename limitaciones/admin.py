from django.contrib import admin
from .models import Limitacion


@admin.register(Limitacion)
class LimitacionAdmin(admin.ModelAdmin):
    list_display   = ('__str__', 'tipo', 'estado', 'profesor', 'asignatura', 'fecha', 'creada_en')
    list_filter    = ('estado', 'tipo', 'fecha')
    search_fields  = ('profesor__username', 'descripcion', 'asignatura__nombre')
    readonly_fields = ('creada_en', 'actualizada_en')
    fieldsets = (
        ('Reporte', {'fields': ('profesor', 'tipo', 'asignatura', 'fecha', 'bloque', 'descripcion')}),
        ('Gestión',  {'fields': ('estado', 'respuesta_decano')}),
        ('Fechas',   {'fields': ('creada_en', 'actualizada_en'), 'classes': ('collapse',)}),
    )
