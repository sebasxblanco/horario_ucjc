from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.db.models import Case, When, Value, IntegerField
from .models import Titulacion, Curso, Asignatura, BloqueHorario, AsignaturaCompartida
from .forms import AsignaturaForm

DIAS = ['Lunes', 'Martes', 'Miércoles', 'Jueves', 'Viernes']
DIA_STR = {1: 'Lunes', 2: 'Martes', 3: 'Miércoles', 4: 'Jueves', 5: 'Viernes'}


def _grid_from_horario(horario, bloques):
    """Construye el grid a partir de las sesiones reales de un HorarioGenerado."""
    from scheduler.models import SesionHorario
    grid = {b.id: {dia: [] for dia in DIAS} for b in bloques}
    sesiones = (
        SesionHorario.objects
        .filter(horario=horario)
        .select_related('asignatura', 'bloque')
        .order_by('dia', 'bloque__hora_inicio')
    )
    for s in sesiones:
        dia_str = DIA_STR.get(s.dia)
        if dia_str and s.bloque_id in grid and dia_str in grid[s.bloque_id]:
            grid[s.bloque_id][dia_str] = [s.asignatura]
    return grid


def _distribuir_en_grid(asignaturas, bloques):
    """
    Distribuye asignaturas en grid[bloque_id][dia] = [asig] | [].
    Garantía: máximo 1 asignatura por celda (bloque × día).
    """
    grid = {b.id: {dia: [] for dia in DIAS} for b in bloques}
    if not bloques or not asignaturas:
        return grid

    DAY_PAIRS = [
        (DIAS[0], DIAS[2]),  # Lun–Mié
        (DIAS[1], DIAS[3]),  # Mar–Jue
        (DIAS[2], DIAS[4]),  # Mié–Vie
        (DIAS[0], DIAS[3]),  # Lun–Jue
        (DIAS[1], DIAS[4]),  # Mar–Vie
    ]
    occupied = set()

    for i, asig in enumerate(asignaturas):
        placed = False
        for b_off in range(len(bloques)):
            b = bloques[(i + b_off) % len(bloques)]
            for d1, d2 in DAY_PAIRS:
                if (b.id, d1) not in occupied and (b.id, d2) not in occupied:
                    grid[b.id][d1] = [asig]
                    grid[b.id][d2] = [asig]
                    occupied.add((b.id, d1))
                    occupied.add((b.id, d2))
                    placed = True
                    break
            if placed:
                break
        if not placed:
            count = 0
            for b in bloques:
                for dia in DIAS:
                    if (b.id, dia) not in occupied:
                        grid[b.id][dia] = [asig]
                        occupied.add((b.id, dia))
                        count += 1
                        if count == 2:
                            break
                if count == 2:
                    break
    return grid


def _get_asignaturas_titulacion(titulacion_sel, curso_sel, semestre):
    """
    Devuelve todas las asignaturas visibles para una titulación:
    las propias del curso + las compartidas desde otra titulación.
    Esto garantiza que IR muestre las 8 asignaturas compartidas con II.
    """
    propias_qs = curso_sel.asignaturas.filter(semestre=semestre)
    compartidas_qs = Asignatura.objects.filter(
        compartidas__titulacion=titulacion_sel,
        semestre=semestre,
        curso__numero=curso_sel.numero,
    )
    return list(
        (propias_qs | compartidas_qs).distinct().order_by('nombre')
    )


def lista_titulaciones(request):
    semestre   = int(request.GET.get('semestre', 1))
    codigo_tit = request.GET.get('titulacion', '')
    num_curso  = request.GET.get('curso', '')

    titulaciones = Titulacion.objects.filter(activa=True).order_by('nombre')
    bloques      = list(BloqueHorario.objects.filter(activo=True).order_by('hora_inicio'))

    titulacion_sel = (
        titulaciones.filter(codigo=codigo_tit).first() if codigo_tit
        else titulaciones.first()
    )

    cursos      = []
    curso_sel   = None
    asignaturas = []
    horario_activo = None
    grid        = {b.id: {dia: [] for dia in DIAS} for b in bloques}

    if titulacion_sel:
        cursos = list(titulacion_sel.cursos.order_by('numero'))
        if num_curso:
            curso_sel = next((c for c in cursos if str(c.numero) == num_curso), None)
        if curso_sel is None and cursos:
            curso_sel = cursos[0]

        if curso_sel:
            # Todas las asignaturas: propias + compartidas (ej: IR ve las 10)
            asignaturas = _get_asignaturas_titulacion(titulacion_sel, curso_sel, semestre)

            # Busca el horario generado más relevante para este contexto
            try:
                from scheduler.models import HorarioGenerado
                horario_activo = (
                    HorarioGenerado.objects
                    .filter(
                        titulacion=titulacion_sel,
                        curso=curso_sel,
                        semestre=semestre,
                        estado__in=['BORRADOR', 'REVISION', 'APROBADO'],
                    )
                    .annotate(
                        prioridad=Case(
                            When(estado='APROBADO',  then=Value(4)),
                            When(estado='REVISION',  then=Value(3)),
                            When(estado='BORRADOR',  then=Value(2)),
                            default=Value(1),
                            output_field=IntegerField(),
                        )
                    )
                    .order_by('-prioridad', '-fecha_generacion')
                    .first()
                )
            except Exception:
                horario_activo = None

            if horario_activo:
                grid = _grid_from_horario(horario_activo, bloques)
            else:
                grid = _distribuir_en_grid(asignaturas, bloques)

    grid_rows = [
        (bloque, [(dia, grid.get(bloque.id, {}).get(dia, [])) for dia in DIAS])
        for bloque in bloques
    ]

    return render(request, 'academic/titulaciones.html', {
        'titulaciones':    titulaciones,
        'titulacion_sel':  titulacion_sel,
        'cursos':          cursos,
        'curso_sel':       curso_sel,
        'semestre':        semestre,
        'dias':            DIAS,
        'grid_rows':       grid_rows,
        'asignaturas':     asignaturas,
        'bloques':         bloques,
        'horario_activo':  horario_activo,
    })


def editar_asignatura(request, pk):
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
        'form': form, 'asignatura': asignatura,
    })


def eliminar_asignatura(request, pk):
    asignatura = get_object_or_404(Asignatura, pk=pk)
    if request.method == 'POST':
        nombre = asignatura.nombre
        asignatura.delete()
        messages.success(request, f'Asignatura «{nombre}» eliminada.')
        return redirect('academic:titulaciones')
    return render(request, 'academic/confirmar_eliminar.html', {'asignatura': asignatura})
