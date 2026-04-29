from django.contrib import admin
from .models import HorarioGenerado, SesionHorario


class SesionInline(admin.TabularInline):
    model = SesionHorario
    extra = 0
    fields = ('dia', 'bloque', 'asignatura', 'aula')
    ordering = ('dia', 'bloque__hora_inicio')


@admin.register(HorarioGenerado)
class HorarioGeneradoAdmin(admin.ModelAdmin):
    list_display  = ('__str__', 'titulacion', 'curso', 'semestre', 'anio_academico', 'estado', 'generado_por', 'fecha_generacion')
    list_filter   = ('estado', 'titulacion', 'semestre', 'anio_academico')
    search_fields = ('titulacion__nombre', 'notas')
    readonly_fields = ('fecha_generacion',)
    inlines = [SesionInline]


@admin.register(SesionHorario)
class SesionHorarioAdmin(admin.ModelAdmin):
    list_display = ('horario', 'dia', 'bloque', 'asignatura', 'aula')
    list_filter  = ('dia', 'horario__titulacion', 'horario__semestre')
