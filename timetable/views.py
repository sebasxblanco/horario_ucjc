from django.shortcuts import render
from academic.models import Titulacion, Asignatura, Profesor


def home(request):
    """Vista principal con resumen del sistema."""
    return render(request, 'home.html', {
        'total_titulaciones': Titulacion.objects.filter(activa=True).count(),
        'total_asignaturas':  Asignatura.objects.count(),
        'total_profesores':   Profesor.objects.count(),
        'titulaciones':       Titulacion.objects.filter(activa=True),
    })