from django.shortcuts import render
from .models import Titulacion


def lista_titulaciones(request):
    """
    Lista todas las titulaciones con sus cursos y asignaturas.
    Usa prefetch_related para optimizar queries — visible en debug-toolbar.
    """
    titulaciones = Titulacion.objects.prefetch_related(
        'cursos__asignaturas'
    ).filter(activa=True)

    return render(request, 'academic/titulaciones.html', {
        'titulaciones': titulaciones
    })