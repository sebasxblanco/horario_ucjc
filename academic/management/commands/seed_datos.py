"""
Seed completo basado en el catálogo oficial 2025-26.
Cubre II (Gininf) y IR (GRobotica) cursos 1-4, semestres 1 y 2.
"""
from django.core.management.base import BaseCommand
from academic.models import (
    Titulacion, Curso, Asignatura, AsignaturaCompartida, BloqueHorario
)
from datetime import time


# ── Bloques horarios ─────────────────────────────────────────────────────────
BLOQUES = [
    ('B1', time(9,  0),  time(11, 0),  'MANANA'),
    ('B2', time(11, 0),  time(13, 0),  'MANANA'),
    ('B3', time(13, 0),  time(15, 0),  'MANANA'),
    ('B4', time(15, 30), time(17, 30), 'TARDE'),
    ('B5', time(17, 30), time(19, 30), 'TARDE'),
    ('B6', time(19, 30), time(21, 30), 'TARDE'),
]

# ── Titulaciones ──────────────────────────────────────────────────────────────
TITULACIONES = [
    ('II', 'Ingeniería Informática', True),
    ('IR', 'Ingeniería Robótica',    True),
]

# ── Cursos ────────────────────────────────────────────────────────────────────
CURSOS = [
    ('II', 1, False), ('II', 2, False), ('II', 3, False), ('II', 4, True),
    ('IR', 1, False), ('IR', 2, False), ('IR', 3, False), ('IR', 4, True),
]

# ── Asignaturas ───────────────────────────────────────────────────────────────
# (codigo, nombre, tit, curso, semestre, es_compartida, matriculados)
ASIGNATURAS = [

    # ══ II – 1º ══════════════════════════════════════════════════════════════
    # S1 (76001-76005)
    ('II-FFIN',  'Fundamentos Físicos de la Informática',          'II', 1, 1, False, 38),
    ('FPROG',    'Fundamentos de Programación',                    'II', 1, 1, True,  65),
    ('II-TPROG', 'Taller de Programación',                         'II', 1, 1, False, 35),
    ('FGES',     'Fundamentos de Gestión Empresarial',             'II', 1, 1, True,  60),
    ('TCOM',     'Tecnología de Computadores',                     'II', 1, 1, True,  55),
    # S2 (76006-76010)
    ('PROG',     'Programación',                                   'II', 1, 2, True,  62),
    ('ALIN',     'Álgebra Lineal',                                 'II', 1, 2, True,  58),
    ('ECOM',     'Estructura de Computadores',                     'II', 1, 2, True,  57),
    ('FSO',      'Fundamentos de Sistemas Operativos',             'II', 1, 2, True,  53),
    ('CMN',      'Cálculo y Métodos Numéricos',                    'II', 1, 2, True,  59),

    # ══ IR – 1º ══════════════════════════════════════════════════════════════
    # S1 (88000-88004): FPROG, FGES, TCOM son compartidas (vinculadas arriba)
    ('IR-FFIS',  'Fundamentos Físicos',                            'IR', 1, 1, False, 28),
    ('IR-FIROB', 'Física para Robótica',                           'IR', 1, 1, False, 25),
    # S2 (88005-88009): PROG, ALIN, ECOM, FSO, CMN son compartidas

    # ══ II – 2º ══════════════════════════════════════════════════════════════
    # S1 (76011-76015)
    ('II2-REDES', 'Redes de Computadores',                         'II', 2, 1, False, 42),
    ('II2-ARQC',  'Arquitectura de Computadores',                  'II', 2, 1, False, 37),
    ('II2-EST',   'Estadística',                                   'II', 2, 1, False, 40),
    ('II2-LAC',   'Lógica, Algoritmia y Computación',              'II', 2, 1, False, 39),
    ('II2-MDIS',  'Matemática Discreta',                           'II', 2, 1, False, 42),
    # S2 (76016-76020)
    ('II2-RSW',   'Redes y Sistemas Web',                          'II', 2, 2, False, 38),
    ('II2-FBD',   'Fundamentos de Bases de Datos',                 'II', 2, 2, False, 40),
    ('II2-EDA',   'Estructura de Datos',                           'II', 2, 2, False, 39),
    ('II2-IPO',   'Interacción Persona-Ordenador',                 'II', 2, 2, False, 36),
    ('II2-FIS',   'Fundamentos de Ingeniería de Software',         'II', 2, 2, False, 38),

    # ══ IR – 2º ══════════════════════════════════════════════════════════════
    # S1 (88010-88014)
    ('IR2-REDES',  'Redes de Computadores',                        'IR', 2, 1, False, 28),
    ('IR2-AUTOM',  'Fundamentos de Automática',                    'IR', 2, 1, False, 30),
    ('IR2-EST',    'Estadística',                                  'IR', 2, 1, False, 27),
    ('IR2-SENS',   'Sensores y Actuadores',                        'IR', 2, 1, False, 28),
    ('IR2-SENYAL', 'Señales y Sistemas',                           'IR', 2, 1, False, 29),
    # S2 (88015-88019)
    ('IR2-ARQC',   'Arquitectura de Computadores',                 'IR', 2, 2, False, 26),
    ('IR2-FBD',    'Fundamentos de Bases de Datos',                'IR', 2, 2, False, 27),
    ('IR2-EDA',    'Estructura de Datos',                          'IR', 2, 2, False, 25),
    ('IR2-CTRL',   'Ingeniería y Sistemas de Control',             'IR', 2, 2, False, 28),
    ('IR2-APRO',   'Aspectos Profesionales de la Robótica',        'IR', 2, 2, False, 24),

    # ══ II – 3º ══════════════════════════════════════════════════════════════
    # S1 (76021-76025)
    ('II3-ASO',   'Administración y Servicios de Sistemas Operativos', 'II', 3, 1, False, 36),
    ('II3-GPS',   'Gestión de Proyectos Software',                 'II', 3, 1, False, 32),
    ('II3-IA',    'Introducción a la Inteligencia Artificial',     'II', 3, 1, False, 35),
    ('II3-SDIST', 'Sistemas Distribuidos',                         'II', 3, 1, False, 34),
    ('II3-LPROG', 'Lenguajes y Paradigmas',                        'II', 3, 1, False, 33),
    # S2 (76026-76031, 76038-76039)
    ('II3-BDA',   'Bases de Datos Avanzadas',                      'II', 3, 2, False, 32),
    ('II3-APRO',  'Aspectos Profesionales de la Informática',      'II', 3, 2, False, 30),
    ('II3-FAA',   'Fundamentos de Aprendizaje Automático',         'II', 3, 2, False, 31),
    ('II3-DSA',   'Desarrollo de Software Avanzado',               'II', 3, 2, False, 25),
    ('II3-IRC',   'Ingeniería de Requisitos y Calidad del SW',     'II', 3, 2, False, 24),
    ('II3-DSIS',  'Desarrollo de Software de Sistemas',            'II', 3, 2, False, 23),
    ('II3-GPI',   'Gestión de Procesos e Infraestructura',         'II', 3, 2, False, 22),

    # ══ IR – 3º ══════════════════════════════════════════════════════════════
    # S1 (88020-88024)
    ('IR3-ASO',   'Administración y Servicios de Sistemas Operativos', 'IR', 3, 1, False, 26),
    ('IR3-MSIM',  'Modelado y Simulación Robótica',                'IR', 3, 1, False, 27),
    ('IR3-IA',    'Introducción a la Inteligencia Artificial',     'IR', 3, 1, False, 27),
    ('IR3-SDIST', 'Sistemas Distribuidos',                         'IR', 3, 1, False, 25),
    ('IR3-EMBOT', 'Sistemas Empotrados en Tiempo Real',            'IR', 3, 1, False, 25),
    # S2 (88025-88029)
    ('IR3-RMOV',  'Robótica Móvil',                                'IR', 3, 2, False, 26),
    ('IR3-RIND',  'Robótica Industrial',                           'IR', 3, 2, False, 25),
    ('IR3-FAA',   'Fundamentos de Aprendizaje Automático',         'IR', 3, 2, False, 24),
    ('IR3-DSIS',  'Desarrollo de Software de Sistemas',            'IR', 3, 2, False, 22),
    ('IR3-PLAN',  'Planificación y Sistemas Robóticos Cognitivos', 'IR', 3, 2, False, 21),

    # ══ II – 4º (solo tarde, es_ultimo=True) ══════════════════════════════════
    # S1 (76033-76037, 76041-76045)
    ('II4-ARQ',   'Arquitectura Software',                         'II', 4, 1, False, 22),
    ('II4-IAPP',  'Integración de Aplicaciones',                   'II', 4, 1, False, 20),
    ('II4-MULT',  'Desarrollo Multiplataforma',                    'II', 4, 1, False, 21),
    ('II4-BD',    'Desarrollo de Servidor y Big Data',             'II', 4, 1, False, 19),
    ('II4-SDN',   'Soluciones y Despliegue en la Nube',            'II', 4, 1, False, 20),
    ('II4-DA',    'Despliegue y Automatización',                   'II', 4, 1, False, 18),
    ('II4-FE',    'Desarrollo de Front-End',                       'II', 4, 1, False, 22),
    ('II4-DAP',   'Diseño y Despliegue de Aplicaciones',           'II', 4, 1, False, 19),
    ('II4-CVE',   'Contenedores, Virtualización y Escalabilidad',  'II', 4, 1, False, 21),
    ('II4-DMN',   'Despliegue y Monitorización en la Nube',        'II', 4, 1, False, 20),
    # S2 (76032, 76040)
    ('II4-SSF',   'Diseño de Software Seguro y Fiable',            'II', 4, 2, False, 18),
    ('II4-CIBER', 'Ciberseguridad en Redes y Aplicaciones',        'II', 4, 2, False, 17),

    # ══ IR – 4º (solo tarde, es_ultimo=True) ══════════════════════════════════
    # S1 (88030-88034)
    ('IR4-A1',  'Asignatura 4º IR 1',  'IR', 4, 1, False, 20),
    ('IR4-A2',  'Asignatura 4º IR 2',  'IR', 4, 1, False, 20),
    ('IR4-A3',  'Asignatura 4º IR 3',  'IR', 4, 1, False, 20),
    ('IR4-A4',  'Asignatura 4º IR 4',  'IR', 4, 1, False, 20),
    ('IR4-A5',  'Asignatura 4º IR 5',  'IR', 4, 1, False, 20),
    # S2 (88035-88039)
    ('IR4-A6',  'Asignatura 4º IR 6',  'IR', 4, 2, False, 20),
    ('IR4-A7',  'Asignatura 4º IR 7',  'IR', 4, 2, False, 20),
    ('IR4-A8',  'Asignatura 4º IR 8',  'IR', 4, 2, False, 20),
    ('IR4-A9',  'Asignatura 4º IR 9',  'IR', 4, 2, False, 20),
    ('IR4-A10', 'Asignatura 4º IR 10', 'IR', 4, 2, False, 20),
]

# Vínculos II ↔ IR para asignaturas compartidas (mismo slot para Doble Grado)
COMPARTIDAS = [
    # 1º S1
    ('FPROG', 'IR'), ('FGES', 'IR'), ('TCOM', 'IR'),
    # 1º S2
    ('PROG',  'IR'), ('ALIN', 'IR'), ('ECOM', 'IR'), ('FSO', 'IR'), ('CMN', 'IR'),
]

# Asignaturas antiguas (II-TI / II-IS) a eliminar tras migrar a II-4
_CODIGOS_OBSOLETOS = [
    'IITI-FE', 'IITI-DMN', 'IITI-CVE', 'IITI-DA', 'IITI-DAM',
    'IIIS-IAPP', 'IIIS-SDN', 'IIIS-BD', 'IIIS-MULT', 'IIIS-ARQ',
]
_TITULACIONES_OBSOLETAS = ['II-TI', 'II-IS']


class Command(BaseCommand):
    help = 'Pobla/actualiza la BD con el catálogo oficial II y IR (2025-26)'

    def handle(self, *args, **kwargs):
        self._cleanup()
        self._seed_bloques()
        self._seed_titulaciones()
        self._seed_cursos()
        self._seed_asignaturas()
        self._seed_compartidas()
        self.stdout.write('\n\033[92m✅  Seed completado.\033[0m\n')

    # ── Limpieza de datos erróneos ────────────────────────────────────────────
    def _cleanup(self):
        self.stdout.write('\n─── Limpieza ───')
        n = Asignatura.objects.filter(codigo__in=_CODIGOS_OBSOLETOS).delete()[0]
        self.stdout.write(f'  Asignaturas obsoletas eliminadas: {n}')
        for cod in _TITULACIONES_OBSOLETAS:
            deleted, _ = Titulacion.objects.filter(codigo=cod).delete()
            if deleted:
                self.stdout.write(f'  Titulación eliminada: {cod}')

    # ── Bloques ───────────────────────────────────────────────────────────────
    def _seed_bloques(self):
        self.stdout.write('\n─── Bloques Horarios ───')
        for nombre, ini, fin, turno in BLOQUES:
            obj, created = BloqueHorario.objects.get_or_create(
                nombre=nombre,
                defaults=dict(hora_inicio=ini, hora_fin=fin, turno=turno, activo=True)
            )
            if not created:
                obj.hora_inicio, obj.hora_fin, obj.turno = ini, fin, turno
                obj.save()
            tag = '✓' if created else '·'
            self.stdout.write(f'  {tag} {nombre}  {ini:%H:%M}–{fin:%H:%M}  ({turno})')

    # ── Titulaciones ──────────────────────────────────────────────────────────
    def _seed_titulaciones(self):
        self.stdout.write('\n─── Titulaciones ───')
        for codigo, nombre, activa in TITULACIONES:
            obj, created = Titulacion.objects.get_or_create(
                codigo=codigo, defaults=dict(nombre=nombre, activa=activa)
            )
            if not created:
                obj.nombre = nombre
                obj.save()
            self.stdout.write(f'  {"✓" if created else "·"} {codigo:<6} {nombre}')

    # ── Cursos ────────────────────────────────────────────────────────────────
    def _seed_cursos(self):
        self.stdout.write('\n─── Cursos ───')
        for tit_cod, num, es_ultimo in CURSOS:
            tit = Titulacion.objects.get(codigo=tit_cod)
            obj, created = Curso.objects.get_or_create(
                titulacion=tit, numero=num,
                defaults=dict(es_ultimo=es_ultimo)
            )
            if not created and obj.es_ultimo != es_ultimo:
                obj.es_ultimo = es_ultimo
                obj.save()
            self.stdout.write(
                f'  {"✓" if created else "·"} {tit_cod} {num}º  (tarde={es_ultimo})'
            )

    # ── Asignaturas ───────────────────────────────────────────────────────────
    def _seed_asignaturas(self):
        self.stdout.write('\n─── Asignaturas ───')
        current_tit = None
        for (codigo, nombre, tit_cod, curso_num,
             semestre, compartida, matriculados) in ASIGNATURAS:
            if tit_cod != current_tit:
                current_tit = tit_cod
                self.stdout.write(f'\n  [{tit_cod}]')
            tit   = Titulacion.objects.get(codigo=tit_cod)
            curso = Curso.objects.get(titulacion=tit, numero=curso_num)
            obj, created = Asignatura.objects.get_or_create(
                codigo=codigo,
                defaults=dict(
                    nombre=nombre, curso=curso, semestre=semestre,
                    horas_sesion=2, sesiones_semana=2,
                    es_compartida=compartida, matriculados=matriculados,
                )
            )
            if not created:
                obj.nombre        = nombre
                obj.curso         = curso
                obj.semestre      = semestre
                obj.es_compartida = compartida
                obj.matriculados  = matriculados
                obj.save()
            tag = '✓' if created else '·'
            self.stdout.write(
                f'    {tag} {codigo:<14} S{semestre}  {nombre}'
            )

    # ── Compartidas ───────────────────────────────────────────────────────────
    def _seed_compartidas(self):
        self.stdout.write('\n─── Vínculos compartidas II ↔ IR ───')
        for asig_cod, tit_extra_cod in COMPARTIDAS:
            try:
                asig    = Asignatura.objects.get(codigo=asig_cod)
                tit_ext = Titulacion.objects.get(codigo=tit_extra_cod)
                _, created = AsignaturaCompartida.objects.get_or_create(
                    asignatura=asig, titulacion=tit_ext
                )
                self.stdout.write(
                    f'  {"↔ NUEVO" if created else "· existe"}  {asig_cod} ↔ {tit_extra_cod}'
                )
            except Asignatura.DoesNotExist:
                self.stdout.write(self.style.WARNING(f'  ⚠ No encontrada: {asig_cod}'))
