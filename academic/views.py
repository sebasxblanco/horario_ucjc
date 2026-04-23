from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from .models import Titulacion, Curso, Asignatura
from .forms import AsignaturaForm

DIAS = ['Lunes', 'Martes', 'Miércoles', 'Jueves', 'Viernes']


def _distribuir_en_grid(asignaturas):
    """
    Distribuye las asignaturas en el grid Mon-Fri.
    Cada asignatura ocupa 2 días (sesiones_semana=2 por defecto, RD-02).
    Devuelve dict: {'Lunes': [asig, ...], 'Martes': [...], ...}
    """
    grid = {dia: [] for dia in DIAS}
    for i, asig in enumerate(asignaturas):
        d1 = i % 5
        d2 = (i + 2) % 5
        if d1 == d2:
            d2 = (d2 + 1) % 5
        grid[DIAS[d1]].append(asig)
        grid[DIAS[d2]].append(asig)
    return grid


def lista_titulaciones(request):
    """
    Vista principal del gestor de asignaturas.
    Muestra un timetable Mon-Fri filtrado por titulación, curso y semestre.
    """
    semestre    = int(request.GET.get('semestre', 1))
    codigo_tit  = request.GET.get('titulacion', '')
    num_curso   = request.GET.get('curso', '')

    titulaciones = Titulacion.objects.filter(activa=True).order_by('nombre')

    # Titulación seleccionada (primera si no hay filtro)
    if codigo_tit:
        titulacion_sel = titulaciones.filter(codigo=codigo_tit).first()
    else:
        titulacion_sel = titulaciones.first()

    cursos        = []
    curso_sel     = None
    asignaturas   = []
    grid          = {dia: [] for dia in DIAS}

    if titulacion_sel:
        cursos = list(titulacion_sel.cursos.order_by('numero'))

        if num_curso:
            curso_sel = next((c for c in cursos if str(c.numero) == num_curso), None)
        if curso_sel is None and cursos:
            curso_sel = cursos[0]

        if curso_sel:
            asignaturas = list(
                curso_sel.asignaturas.filter(semestre=semestre).order_by('nombre')
            )
            grid = _distribuir_en_grid(asignaturas)

    return render(request, 'academic/titulaciones.html', {
        'titulaciones':  titulaciones,
        'titulacion_sel': titulacion_sel,
        'cursos':        cursos,
        'curso_sel':     curso_sel,
        'semestre':      semestre,
        'dias':          DIAS,
        'grid':          grid,
        'asignaturas':   asignaturas,
    })


def editar_asignatura(request, pk):
    """Editar una asignatura existente."""
    asignatura = get_object_or_404(Asignatura, pk=pk)

    if request.method == 'POST':
        form = AsignaturaForm(request.POST, instance=asignatura)
        if form.is_valid():
            form.save()
            messages.success(request, f'Asignatura «{asignatura.nombre}» actualizada.')
            return redirect('academic:titulaciones')
    else:
        form = AsignaturaForm(instance=asignatura)

    return render(request, 'academic/editar_asignatura.html', {
        'form': form,
        'asignatura': asignatura,
    })


def eliminar_asignatura(request, pk):
    """Confirmación y eliminación de una asignatura."""
    asignatura = get_object_or_404(Asignatura, pk=pk)

    if request.method == 'POST':
        nombre = asignatura.nombre
        asignatura.delete()
        messages.success(request, f'Asignatura «{nombre}» eliminada.')
        return redirect('academic:titulaciones')

    return render(request, 'academic/confirmar_eliminar.html', {
        'asignatura': asignatura,
    })
