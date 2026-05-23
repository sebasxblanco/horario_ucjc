import json
from functools import wraps
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import HttpResponseForbidden

from academic.models import Titulacion, Curso, Asignatura
from .models import HorarioGenerado, SesionHorario
from .algorithm import generar_horario, hay_conflictos

DIAS_LABEL = {1:'Lunes', 2:'Martes', 3:'Miércoles', 4:'Jueves', 5:'Viernes'}
DIAS = [1, 2, 3, 4, 5]


# ── Decorador de rol ──────────────────────────────────────────────────────

def rol_requerido(*roles):
    """Permite el acceso solo a usuarios con alguno de los roles indicados."""
    def decorator(view_func):
        @wraps(view_func)
        @login_required(login_url='/accounts/login/')
        def wrapped(request, *args, **kwargs):
            if request.user.is_superuser:
                return view_func(request, *args, **kwargs)
            if hasattr(request.user, 'rol') and request.user.rol in roles:
                return view_func(request, *args, **kwargs)
            return HttpResponseForbidden(
                render(request, 'scheduler/403.html', status=403).content
            )
        return wrapped
    return decorator


# ── Vista: generar horario (solo Decano / IT) ─────────────────────────────

@rol_requerido('DECANO', 'IT')
def generar(request):
    titulaciones = Titulacion.objects.filter(activa=True).order_by('nombre')

    if request.method == 'POST':
        tit_codigo   = request.POST.get('titulacion', '').strip()
        curso_num    = request.POST.get('curso', '').strip()
        semestre_raw = request.POST.get('semestre', '').strip()
        anio         = request.POST.get('anio_academico', '2024-25').strip()

        if not tit_codigo or not curso_num or not semestre_raw:
            messages.error(request, 'Debes seleccionar titulación, curso y semestre.')
            return redirect('scheduler:generar')

        semestre     = int(semestre_raw)
        umbral_foro  = int(request.POST.get('umbral_foro', 0) or 0)
        tit    = get_object_or_404(Titulacion, codigo=tit_codigo)
        curso  = get_object_or_404(Curso, titulacion=tit, numero=int(curso_num))

        horario, conflictos = generar_horario(tit, curso, semestre, anio, request.user, umbral_foro)

        if conflictos:
            for c in conflictos:
                messages.warning(request, c)

        if horario:
            messages.success(request, f'Horario generado: {horario}')
            return redirect('scheduler:detalle', pk=horario.pk)
        else:
            messages.error(request, 'No se pudo generar el horario.')

    # GET — formulario
    cursos_por_tit_json = json.dumps({
        t.codigo: [
            {'numero': c.numero, 'es_ultimo': c.es_ultimo}
            for c in t.cursos.order_by('numero')
        ]
        for t in titulaciones
    })

    matriculados_json = json.dumps({
        codigo: mat
        for codigo, mat in Asignatura.objects.filter(es_compartida=True).values_list('codigo', 'matriculados')
    })

    return render(request, 'scheduler/generar.html', {
        'titulaciones':        titulaciones,
        'cursos_por_tit_json': cursos_por_tit_json,
        'matriculados_json':   matriculados_json,
    })


# ── Vista: lista de horarios ──────────────────────────────────────────────

@login_required(login_url='/accounts/login/')
def lista(request):
    qs = HorarioGenerado.objects.select_related('titulacion', 'curso', 'generado_por')

    # Alumnos solo ven los aprobados
    if hasattr(request.user, 'rol') and request.user.rol == 'ESTUDIANTE':
        qs = qs.filter(estado=HorarioGenerado.Estado.APROBADO)

    titulaciones = Titulacion.objects.filter(activa=True)
    tit_filtro = request.GET.get('titulacion', '')
    sem_filtro = request.GET.get('semestre', '')

    if tit_filtro:
        qs = qs.filter(titulacion__codigo=tit_filtro)
    if sem_filtro:
        qs = qs.filter(semestre=sem_filtro)

    return render(request, 'scheduler/lista.html', {
        'horarios':    qs,
        'titulaciones': titulaciones,
        'tit_filtro':  tit_filtro,
        'sem_filtro':  sem_filtro,
        'es_admin':    _es_admin(request.user),
    })


# ── Vista: detalle / timetable de un horario ─────────────────────────────

@login_required(login_url='/accounts/login/')
def detalle(request, pk):
    horario = get_object_or_404(HorarioGenerado, pk=pk)

    # Alumnos solo ven aprobados
    if (hasattr(request.user, 'rol') and request.user.rol == 'ESTUDIANTE'
            and horario.estado != HorarioGenerado.Estado.APROBADO):
        return HttpResponseForbidden(
            render(request, 'scheduler/403.html', status=403).content
        )

    sesiones = horario.sesiones.select_related(
        'asignatura', 'bloque',
        'asignatura__asignacion__profesor__user',
    ).order_by(
        'dia', 'bloque__hora_inicio'
    )

    # Construye grid[dia][bloque_id] = sesion
    from academic.models import BloqueHorario
    bloques = BloqueHorario.objects.filter(activo=True).order_by('hora_inicio')
    if horario.curso.es_ultimo:
        bloques = bloques.filter(turno='TARDE')

    grid = {dia: {b.id: None for b in bloques} for dia in DIAS}
    for s in sesiones:
        if s.dia in grid and s.bloque_id in grid[s.dia]:
            grid[s.dia][s.bloque_id] = s

    conflictos = hay_conflictos(horario) if _es_admin(request.user) else []

    return render(request, 'scheduler/detalle.html', {
        'horario':    horario,
        'dias':       DIAS,
        'dias_label': DIAS_LABEL,
        'bloques':    bloques,
        'grid':       grid,
        'conflictos': conflictos,
        'es_admin':   _es_admin(request.user),
    })


# ── Workflow: cambiar estado (solo Decano) ────────────────────────────────

@rol_requerido('DECANO', 'IT')
def cambiar_estado(request, pk):
    if request.method != 'POST':
        return redirect('scheduler:detalle', pk=pk)

    horario      = get_object_or_404(HorarioGenerado, pk=pk)
    nuevo_estado = request.POST.get('estado')
    notas        = request.POST.get('notas', '').strip()

    estados_validos = [e.value for e in HorarioGenerado.Estado]
    if nuevo_estado not in estados_validos:
        messages.error(request, 'Estado no válido.')
        return redirect('scheduler:detalle', pk=pk)

    horario.estado = nuevo_estado
    if notas:
        horario.notas = notas
    horario.save()
    messages.success(request, f'Estado actualizado a «{horario.get_estado_display()}».')
    return redirect('scheduler:detalle', pk=pk)


# ── Eliminar borrador (solo Decano/IT) ────────────────────────────────────

@rol_requerido('DECANO', 'IT')
def eliminar(request, pk):
    horario = get_object_or_404(HorarioGenerado, pk=pk)
    if request.method == 'POST':
        if horario.es_editable:
            horario.delete()
            messages.success(request, 'Horario eliminado.')
            return redirect('scheduler:lista')
        messages.error(request, 'Solo se pueden eliminar borradores.')
    return redirect('scheduler:detalle', pk=pk)


# ── Limpiar borradores (solo Decano/IT) ──────────────────────────────────

@rol_requerido('DECANO', 'IT')
def limpiar(request):
    if request.method == 'POST':
        scope = request.POST.get('scope', 'borradores')
        if scope == 'todo':
            n, _ = HorarioGenerado.objects.all().delete()
        else:
            n, _ = HorarioGenerado.objects.filter(
                estado__in=[HorarioGenerado.Estado.BORRADOR, HorarioGenerado.Estado.RECHAZADO]
            ).delete()
        messages.success(request, f'{n} horario(s) eliminado(s).')
    return redirect('scheduler:lista')


# ── Helper ────────────────────────────────────────────────────────────────

def _es_admin(user):
    if user.is_superuser:
        return True
    return hasattr(user, 'rol') and user.rol in ('DECANO', 'IT', 'CONSULTOR')
