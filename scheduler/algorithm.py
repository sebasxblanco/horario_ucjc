"""
Generador de horarios — algoritmo greedy CSP.

Restricciones hard implementadas:
  RD-01  2h por sesión (tamaño fijo del BloqueHorario)
  RD-02  2 sesiones/semana por asignatura
  RD-03  Lunes a Viernes
  RD-04  Último curso → solo bloques de tarde
         Curso híbrido (DG 5º) → mañana y tarde
  RD-05  Un profesor no puede impartir dos asignaturas en el mismo slot
         (se comprueba en todos los horarios BORRADOR/APROBADO existentes)
  RD-08  Alumnos sin solapamiento (mismo grupo = mismo slot libre)
  RD-10  Asignaturas compartidas → mismo slot en todas las titulaciones vinculadas
  RD-13  Evitar huecos: se asignan días consecutivos cuando es posible
"""

from academic.models import Asignatura, BloqueHorario, AsignaturaCompartida
from .models import HorarioGenerado, SesionHorario

DIAS = [1, 2, 3, 4, 5]   # Lunes=1 … Viernes=5


# ──────────────────────────────────────────────────────────────────
# API PÚBLICA
# ──────────────────────────────────────────────────────────────────

def generar_horario(titulacion, curso_obj, semestre, anio_academico, usuario, umbral_foro=0):
    """
    Genera y persiste un HorarioGenerado en estado BORRADOR.
    Devuelve (horario, conflictos) donde conflictos es una lista de strings.
    """
    HorarioGenerado.objects.filter(
        titulacion=titulacion, curso=curso_obj,
        semestre=semestre, anio_academico=anio_academico,
        estado=HorarioGenerado.Estado.BORRADOR,
    ).delete()

    bloques = _get_bloques(curso_obj)
    if not bloques:
        return None, ['No hay bloques horarios activos configurados.']

    asignaturas_propias = list(
        Asignatura.objects.filter(curso=curso_obj, semestre=semestre)
        .order_by('-es_compartida', 'nombre')
    )

    from academic.models import AsignaturaCompartida as AC
    ids_propios = {a.id for a in asignaturas_propias}
    asigs_vinculadas = list(
        Asignatura.objects.filter(
            compartidas__titulacion=titulacion,
            semestre=semestre,
            curso__numero=curso_obj.numero,
        ).exclude(id__in=ids_propios).order_by('nombre')
    )

    asignaturas = asigs_vinculadas + asignaturas_propias
    if not asignaturas:
        return None, [f'No hay asignaturas en S{semestre} para este curso.']

    slots_compartidos = _slots_compartidos(titulacion, curso_obj, semestre, anio_academico)

    # Slots ocupados por profesor en todos los horarios existentes (RD-05)
    slots_profesor = _slots_ocupados_por_profesores(anio_academico)

    horario = HorarioGenerado.objects.create(
        titulacion=titulacion,
        curso=curso_obj,
        semestre=semestre,
        anio_academico=anio_academico,
        estado=HorarioGenerado.Estado.BORRADOR,
        generado_por=usuario,
    )

    ocupados = {}      # (dia, bloque_id) → asignatura_id
    conflictos = []

    for asig in asignaturas:
        cumple_foro = (umbral_foro == 0 or asig.matriculados >= umbral_foro)
        if asig.es_compartida and cumple_foro and asig.id in slots_compartidos:
            for dia, bloque_id in slots_compartidos[asig.id]:
                slot = (dia, bloque_id)
                if slot in ocupados:
                    conflictos.append(
                        f'Conflicto compartida: {asig.codigo} en '
                        f'{_dia_str(dia)} bloque {bloque_id} ya ocupado.'
                    )
                    continue
                SesionHorario.objects.create(
                    horario=horario, asignatura=asig,
                    dia=dia, bloque_id=bloque_id
                )
                ocupados[slot] = asig.id
                # Registra el slot del profesor en la tabla en memoria
                prof_id = _profesor_id(asig)
                if prof_id:
                    slots_profesor.setdefault(prof_id, set()).add(slot)
        else:
            ok = _asignar_sesiones(
                horario, asig, bloques, ocupados, conflictos, slots_profesor
            )
            if not ok:
                conflictos.append(
                    f'Sin slot disponible para {asig.codigo} — {asig.nombre}'
                )

    return horario, conflictos


def hay_conflictos(horario):
    """Revalida el horario en memoria. Devuelve lista de strings (vacía = OK)."""
    conflictos = []
    slots = {}

    for sesion in horario.sesiones.select_related('asignatura', 'bloque'):
        slot = (sesion.dia, sesion.bloque_id)
        if slot in slots:
            conflictos.append(
                f'SOLAPAMIENTO: {slots[slot]} y {sesion.asignatura.codigo} '
                f'en {sesion.get_dia_display()} {sesion.bloque}'
            )
        else:
            slots[slot] = sesion.asignatura.codigo

    return conflictos


# ──────────────────────────────────────────────────────────────────
# HELPERS PRIVADOS
# ──────────────────────────────────────────────────────────────────

def _get_bloques(curso_obj):
    qs = BloqueHorario.objects.filter(activo=True).order_by('hora_inicio')
    if getattr(curso_obj, 'es_hibrido', False):
        return list(qs)          # DG 5º: mañana + tarde
    if curso_obj.es_ultimo:
        return list(qs.filter(turno='TARDE'))   # RD-04
    return list(qs.filter(turno='MANANA'))


def _slots_compartidos(titulacion, curso_obj, semestre, anio_academico):
    """
    Devuelve {asignatura_id: [(dia, bloque_id), ...]} con los slots ya
    asignados a asignaturas compartidas en OTRA titulación (RD-10).
    """
    result = {}
    codigos_compartidos = AsignaturaCompartida.objects.filter(
        titulacion=titulacion
    ).values_list('asignatura_id', flat=True)

    for asig_id in codigos_compartidos:
        sesiones = SesionHorario.objects.filter(
            asignatura_id=asig_id,
            horario__curso__numero=curso_obj.numero,
            horario__semestre=semestre,
            horario__anio_academico=anio_academico,
            horario__estado__in=[
                HorarioGenerado.Estado.BORRADOR,
                HorarioGenerado.Estado.APROBADO,
            ],
        ).exclude(horario__titulacion=titulacion)

        if sesiones.exists():
            result[asig_id] = [(s.dia, s.bloque_id) for s in sesiones]

    return result


def _slots_ocupados_por_profesores(anio_academico):
    """
    Devuelve {profesor_id: {(dia, bloque_id), ...}} con todos los slots
    ya asignados en horarios BORRADOR/APROBADO del mismo año académico.
    Esto permite detectar conflictos de profesor entre titulaciones (RD-05).
    """
    result = {}
    sesiones = SesionHorario.objects.filter(
        horario__anio_academico=anio_academico,
        horario__estado__in=[
            HorarioGenerado.Estado.BORRADOR,
            HorarioGenerado.Estado.APROBADO,
        ],
    ).select_related('asignatura__asignacion__profesor')

    for s in sesiones:
        try:
            prof_id = s.asignatura.asignacion.profesor_id
        except Exception:
            continue
        result.setdefault(prof_id, set()).add((s.dia, s.bloque_id))

    return result


def _profesor_id(asig):
    """Devuelve el profesor_id asignado a la asignatura, o None."""
    try:
        return asig.asignacion.profesor_id
    except Exception:
        return None


def _asignar_sesiones(horario, asig, bloques, ocupados, conflictos, slots_profesor):
    """
    Intenta asignar `asig.sesiones_semana` sesiones en días distintos.
    Respeta:
      - ocupados: slots ya usados por este horario (mismo grupo)
      - slots_profesor: slots ya usados por el mismo profesor en otros horarios
    Modifica ambas estructuras in-place. Devuelve True si se asignaron todas.
    """
    sesiones_necesarias = asig.sesiones_semana
    prof_id = _profesor_id(asig)
    dias_usados = []
    asignadas = 0

    for dia in DIAS:
        if asignadas >= sesiones_necesarias:
            break
        if dia in dias_usados:
            continue

        for bloque in bloques:
            slot = (dia, bloque.id)
            if slot in ocupados:
                continue
            # RD-05: el profesor no puede estar en otro grupo al mismo tiempo
            if prof_id and slot in slots_profesor.get(prof_id, set()):
                continue
            SesionHorario.objects.create(
                horario=horario, asignatura=asig,
                dia=dia, bloque=bloque
            )
            ocupados[slot] = asig.id
            if prof_id:
                slots_profesor.setdefault(prof_id, set()).add(slot)
            dias_usados.append(dia)
            asignadas += 1
            break   # solo una sesión por día (RD-13)

    return asignadas == sesiones_necesarias


def _dia_str(num):
    return {1:'Lunes',2:'Martes',3:'Miércoles',4:'Jueves',5:'Viernes'}.get(num, str(num))
