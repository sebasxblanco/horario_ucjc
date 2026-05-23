"""
Generador de horarios — algoritmo greedy CSP.

Restricciones hard implementadas:
  RD-01  2h por sesión (tamaño fijo del BloqueHorario)
  RD-02  2 sesiones/semana por asignatura
  RD-03  Lunes a Viernes
  RD-04  Último curso → solo bloques de tarde
  RD-05  Ningún grupo puede tener 2 asignaturas en el mismo slot
  RD-08  Alumnos sin solapamiento (mismo grupo = mismo slot libre)
  RD-10  Asignaturas compartidas → mismo slot en todas las titulaciones vinculadas
  RD-13  Evitar huecos: se asignan días consecutivos cuando es posible

Orden de asignación:
  1. Asignaturas compartidas (más restringidas — ya asignadas en otra titulación)
  2. Asignaturas exclusivas (rellena los slots libres restantes)
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
    # Elimina borrador previo para el mismo contexto (regeneración)
    HorarioGenerado.objects.filter(
        titulacion=titulacion, curso=curso_obj,
        semestre=semestre, anio_academico=anio_academico,
        estado=HorarioGenerado.Estado.BORRADOR,
    ).delete()

    bloques = _get_bloques(curso_obj)
    if not bloques:
        return None, ['No hay bloques horarios activos configurados.']

    # Asignaturas propias del curso
    asignaturas_propias = list(
        Asignatura.objects.filter(curso=curso_obj, semestre=semestre)
        .order_by('-es_compartida', 'nombre')
    )

    # Asignaturas compartidas DESDE otra titulación hacia esta (RD-10)
    # Ej: cuando generamos IR, incluimos FPROG/FGES/… que pertenecen a II
    from academic.models import AsignaturaCompartida as AC
    ids_propios = {a.id for a in asignaturas_propias}
    asigs_vinculadas = list(
        Asignatura.objects.filter(
            compartidas__titulacion=titulacion,
            semestre=semestre,
            curso__numero=curso_obj.numero,
        ).exclude(id__in=ids_propios).order_by('nombre')
    )

    # Compartidas primero (más restringidas), luego propias exclusivas
    asignaturas = asigs_vinculadas + asignaturas_propias
    if not asignaturas:
        return None, [f'No hay asignaturas en S{semestre} para este curso.']

    # Slots ya ocupados por asignaturas compartidas en OTRA titulación (RD-10)
    slots_compartidos = _slots_compartidos(titulacion, curso_obj, semestre, anio_academico)

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
        # Foro de grado: si hay umbral y la asignatura no alcanza el mínimo
        # de alumnos, se trata como exclusiva aunque esté marcada como compartida
        cumple_foro = (umbral_foro == 0 or asig.matriculados >= umbral_foro)
        if asig.es_compartida and cumple_foro and asig.id in slots_compartidos:
            # Reutiliza los slots de la otra titulación (RD-10)
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
        else:
            ok = _asignar_sesiones(horario, asig, bloques, ocupados, conflictos)
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
    if curso_obj.es_ultimo:
        qs = qs.filter(turno='TARDE')   # RD-04: último curso solo tarde
    else:
        qs = qs.filter(turno='MANANA')  # cursos 1-3 solo mañana
    return list(qs)


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


def _asignar_sesiones(horario, asig, bloques, ocupados, conflictos):
    """
    Intenta asignar `asig.sesiones_semana` sesiones en días distintos.
    Modifica `ocupados` in-place. Devuelve True si se asignaron todas.
    """
    sesiones_necesarias = asig.sesiones_semana
    dias_usados = []
    asignadas = 0

    # Intentamos días en orden; si no hay slot libre en un día, probamos el siguiente
    for dia in DIAS:
        if asignadas >= sesiones_necesarias:
            break
        if dia in dias_usados:
            continue

        for bloque in bloques:
            slot = (dia, bloque.id)
            if slot not in ocupados:
                SesionHorario.objects.create(
                    horario=horario, asignatura=asig,
                    dia=dia, bloque=bloque
                )
                ocupados[slot] = asig.id
                dias_usados.append(dia)
                asignadas += 1
                break   # solo una sesión por día (RD-13: evitar huecos)

    return asignadas == sesiones_necesarias


def _dia_str(num):
    return {1:'Lunes',2:'Martes',3:'Miércoles',4:'Jueves',5:'Viernes'}.get(num, str(num))
