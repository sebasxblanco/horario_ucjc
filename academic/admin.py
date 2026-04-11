from django.contrib import admin
from .models import (Titulacion, Curso, Asignatura, AsignaturaCompartida,
                     Profesor, DisponibilidadProfesor, BloqueHorario,
                     AsignacionProfesorAsignatura)


@admin.register(Titulacion)
class TitulacionAdmin(admin.ModelAdmin):
    list_display = ('codigo', 'nombre', 'activa')


@admin.register(Curso)
class CursoAdmin(admin.ModelAdmin):
    list_display = ('titulacion', 'numero', 'es_ultimo')


@admin.register(Asignatura)
class AsignaturaAdmin(admin.ModelAdmin):
    list_display = ('codigo', 'nombre', 'curso', 'es_compartida')


@admin.register(Profesor)
class ProfesorAdmin(admin.ModelAdmin):
    list_display = ('user', 'departamento')


admin.site.register(AsignaturaCompartida)
admin.site.register(DisponibilidadProfesor)
admin.site.register(BloqueHorario)
admin.site.register(AsignacionProfesorAsignatura)