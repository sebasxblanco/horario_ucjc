"""
Seed completo basado en el catálogo oficial 2025-26.
Cubre II (GInInf), IR (GRobotica), IT (GTelemática) y DG (Doble Grado II+IR).
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
    ('II', 'Ingeniería Informática',        True),
    ('IR', 'Ingeniería Robótica',           True),
    ('IT', 'Ingeniería Telemática',         True),
    ('DG', 'Doble Grado Informática+Robótica', True),
]

# ── Cursos ────────────────────────────────────────────────────────────────────
# (tit_cod, numero, es_ultimo, es_hibrido)
CURSOS = [
    # II — 4 años, último solo tarde
    ('II', 1, False, False), ('II', 2, False, False),
    ('II', 3, False, False), ('II', 4, True,  False),
    # IR — 4 años, último solo tarde
    ('IR', 1, False, False), ('IR', 2, False, False),
    ('IR', 3, False, False), ('IR', 4, True,  False),
    # IT — 4 años, último solo tarde
    ('IT', 1, False, False), ('IT', 2, False, False),
    ('IT', 3, False, False), ('IT', 4, True,  False),
    # DG — 5 años, último híbrido (mañana + tarde)
    ('DG', 1, False, False), ('DG', 2, False, False),
    ('DG', 3, False, False), ('DG', 4, False, False),
    ('DG', 5, True,  True),
]

# ── Asignaturas ───────────────────────────────────────────────────────────────
# (codigo, nombre, tit, curso, semestre, es_compartida, matriculados)
ASIGNATURAS = [

    # ══ II – 1º ══════════════════════════════════════════════════════════════
    ('II-FFIN',  'Fundamentos Físicos de la Informática',          'II', 1, 1, False, 38),
    ('FPROG',    'Fundamentos de Programación',                    'II', 1, 1, True,  65),
    ('II-TPROG', 'Taller de Programación',                         'II', 1, 1, False, 35),
    ('FGES',     'Fundamentos de Gestión Empresarial',             'II', 1, 1, True,  60),
    ('TCOM',     'Tecnología de Computadores',                     'II', 1, 1, True,  55),
    ('PROG',     'Programación',                                   'II', 1, 2, True,  62),
    ('ALIN',     'Álgebra Lineal',                                 'II', 1, 2, True,  58),
    ('ECOM',     'Estructura de Computadores',                     'II', 1, 2, True,  57),
    ('FSO',      'Fundamentos de Sistemas Operativos',             'II', 1, 2, True,  53),
    ('CMN',      'Cálculo y Métodos Numéricos',                    'II', 1, 2, True,  59),

    # ══ IR – 1º ══════════════════════════════════════════════════════════════
    ('IR-FFIS',  'Fundamentos Físicos',                            'IR', 1, 1, False, 28),
    ('IR-FIROB', 'Física para Robótica',                           'IR', 1, 1, False, 25),

    # ══ IT – 1º ══════════════════════════════════════════════════════════════
    ('IT-CALC1', 'Cálculo I',                                      'IT', 1, 1, False, 32),
    ('IT-TELEC', 'Fundamentos de Telecomunicaciones',              'IT', 1, 1, False, 30),
    ('IT-ELEG',  'Electrónica General',                            'IT', 1, 1, False, 29),
    # FPROG y TCOM compartidas desde II (vínculos en COMPARTIDAS)
    ('IT-CALC2', 'Cálculo II',                                     'IT', 1, 2, False, 31),
    ('IT-TELDIG','Telecomunicaciones Digitales',                   'IT', 1, 2, False, 28),
    ('IT-EANA',  'Electrónica Analógica',                          'IT', 1, 2, False, 27),
    # PROG y CMN compartidas desde II

    # ══ DG – 1º ══════════════════════════════════════════════════════════════
    ('DG1-CALC1','Cálculo I',                                      'DG', 1, 1, False, 22),
    ('DG1-MAT1', 'Matemáticas I',                                  'DG', 1, 1, False, 22),
    # FPROG, FGES, TCOM compartidas desde II
    ('DG1-FIROB','Física para Robótica',                           'DG', 1, 1, False, 20),
    ('DG1-CALC2','Cálculo II',                                     'DG', 1, 2, False, 21),
    ('DG1-MAT2', 'Matemáticas II',                                 'DG', 1, 2, False, 21),
    # PROG, ALIN, ECOM, FSO compartidas desde II

    # ══ II – 2º ══════════════════════════════════════════════════════════════
    ('II2-REDES', 'Redes de Computadores',                         'II', 2, 1, False, 42),
    ('II2-ARQC',  'Arquitectura de Computadores',                  'II', 2, 1, False, 37),
    ('II2-EST',   'Estadística',                                   'II', 2, 1, False, 40),
    ('II2-LAC',   'Lógica, Algoritmia y Computación',              'II', 2, 1, False, 39),
    ('II2-MDIS',  'Matemática Discreta',                           'II', 2, 1, False, 42),
    ('II2-RSW',   'Redes y Sistemas Web',                          'II', 2, 2, False, 38),
    ('II2-FBD',   'Fundamentos de Bases de Datos',                 'II', 2, 2, False, 40),
    ('II2-EDA',   'Estructura de Datos',                           'II', 2, 2, False, 39),
    ('II2-IPO',   'Interacción Persona-Ordenador',                 'II', 2, 2, False, 36),
    ('II2-FIS',   'Fundamentos de Ingeniería de Software',         'II', 2, 2, False, 38),

    # ══ IR – 2º ══════════════════════════════════════════════════════════════
    ('IR2-REDES',  'Redes de Computadores',                        'IR', 2, 1, False, 28),
    ('IR2-AUTOM',  'Fundamentos de Automática',                    'IR', 2, 1, False, 30),
    ('IR2-EST',    'Estadística',                                  'IR', 2, 1, False, 27),
    ('IR2-SENS',   'Sensores y Actuadores',                        'IR', 2, 1, False, 28),
    ('IR2-SENYAL', 'Señales y Sistemas',                           'IR', 2, 1, False, 29),
    ('IR2-ARQC',   'Arquitectura de Computadores',                 'IR', 2, 2, False, 26),
    ('IR2-FBD',    'Fundamentos de Bases de Datos',                'IR', 2, 2, False, 27),
    ('IR2-EDA',    'Estructura de Datos',                          'IR', 2, 2, False, 25),
    ('IR2-CTRL',   'Ingeniería y Sistemas de Control',             'IR', 2, 2, False, 28),
    ('IR2-APRO',   'Aspectos Profesionales de la Robótica',        'IR', 2, 2, False, 24),

    # ══ IT – 2º ══════════════════════════════════════════════════════════════
    ('IT2-SENYAL', 'Señales y Sistemas',                           'IT', 2, 1, False, 30),
    ('IT2-REDES',  'Redes de Comunicaciones I',                    'IT', 2, 1, False, 31),
    ('IT2-SO',     'Sistemas Operativos',                          'IT', 2, 1, False, 29),
    ('IT2-EST',    'Estadística',                                  'IT', 2, 1, False, 28),
    ('IT2-PROG',   'Programación de Sistemas',                     'IT', 2, 1, False, 27),
    ('IT2-REDII',  'Redes de Comunicaciones II',                   'IT', 2, 2, False, 30),
    ('IT2-TRANS',  'Transmisión Digital',                          'IT', 2, 2, False, 28),
    ('IT2-BD',     'Bases de Datos',                               'IT', 2, 2, False, 27),
    ('IT2-SEGIN',  'Seguridad Informática',                        'IT', 2, 2, False, 26),
    ('IT2-ARQC',   'Arquitectura de Computadores',                 'IT', 2, 2, False, 29),

    # ══ DG – 2º ══════════════════════════════════════════════════════════════
    ('DG2-AUTOM',  'Fundamentos de Automática',                    'DG', 2, 1, False, 20),
    ('DG2-SENS',   'Sensores y Actuadores',                        'DG', 2, 1, False, 20),
    ('DG2-EST',    'Estadística',                                  'DG', 2, 1, False, 20),
    ('DG2-SENYAL', 'Señales y Sistemas',                           'DG', 2, 1, False, 20),
    ('DG2-REDES',  'Redes de Computadores',                        'DG', 2, 1, False, 20),
    ('DG2-ARQC',   'Arquitectura de Computadores',                 'DG', 2, 1, False, 20),
    ('DG2-CTRL',   'Ingeniería y Sistemas de Control',             'DG', 2, 2, False, 20),
    ('DG2-FBD',    'Fundamentos de Bases de Datos',                'DG', 2, 2, False, 20),
    ('DG2-EDA',    'Estructura de Datos',                          'DG', 2, 2, False, 20),
    ('DG2-IPO',    'Interacción Persona-Ordenador',                'DG', 2, 2, False, 20),
    ('DG2-FIS',    'Fundamentos de Ingeniería de Software',        'DG', 2, 2, False, 20),
    ('DG2-APRO',   'Aspectos Profesionales',                       'DG', 2, 2, False, 20),

    # ══ II – 3º ══════════════════════════════════════════════════════════════
    ('II3-ASO',   'Administración y Servicios de Sistemas Operativos', 'II', 3, 1, False, 36),
    ('II3-GPS',   'Gestión de Proyectos Software',                 'II', 3, 1, False, 32),
    ('II3-IA',    'Introducción a la Inteligencia Artificial',     'II', 3, 1, False, 35),
    ('II3-SDIST', 'Sistemas Distribuidos',                         'II', 3, 1, False, 34),
    ('II3-LPROG', 'Lenguajes y Paradigmas',                        'II', 3, 1, False, 33),
    ('II3-BDA',   'Bases de Datos Avanzadas',                      'II', 3, 2, False, 32),
    ('II3-APRO',  'Aspectos Profesionales de la Informática',      'II', 3, 2, False, 30),
    ('II3-FAA',   'Fundamentos de Aprendizaje Automático',         'II', 3, 2, False, 31),
    ('II3-DSA',   'Desarrollo de Software Avanzado',               'II', 3, 2, False, 25),
    ('II3-IRC',   'Ingeniería de Requisitos y Calidad del SW',     'II', 3, 2, False, 24),
    ('II3-DSIS',  'Desarrollo de Software de Sistemas',            'II', 3, 2, False, 23),
    ('II3-GPI',   'Gestión de Procesos e Infraestructura',         'II', 3, 2, False, 22),

    # ══ IR – 3º ══════════════════════════════════════════════════════════════
    ('IR3-ASO',   'Administración y Servicios de Sistemas Operativos', 'IR', 3, 1, False, 26),
    ('IR3-MSIM',  'Modelado y Simulación Robótica',                'IR', 3, 1, False, 27),
    ('IR3-IA',    'Introducción a la Inteligencia Artificial',     'IR', 3, 1, False, 27),
    ('IR3-SDIST', 'Sistemas Distribuidos',                         'IR', 3, 1, False, 25),
    ('IR3-EMBOT', 'Sistemas Empotrados en Tiempo Real',            'IR', 3, 1, False, 25),
    ('IR3-RMOV',  'Robótica Móvil',                                'IR', 3, 2, False, 26),
    ('IR3-RIND',  'Robótica Industrial',                           'IR', 3, 2, False, 25),
    ('IR3-FAA',   'Fundamentos de Aprendizaje Automático',         'IR', 3, 2, False, 24),
    ('IR3-DSIS',  'Desarrollo de Software de Sistemas',            'IR', 3, 2, False, 22),
    ('IR3-PLAN',  'Planificación y Sistemas Robóticos Cognitivos', 'IR', 3, 2, False, 21),

    # ══ IT – 3º ══════════════════════════════════════════════════════════════
    ('IT3-INAL',  'Redes Inalámbricas',                            'IT', 3, 1, False, 27),
    ('IT3-VOZIP', 'Voz sobre IP y Multimedia',                     'IT', 3, 1, False, 25),
    ('IT3-CSEG',  'Ciberseguridad I',                              'IT', 3, 1, False, 26),
    ('IT3-GRED',  'Gestión y Administración de Redes',             'IT', 3, 1, False, 24),
    ('IT3-SERV',  'Servicios de Internet',                         'IT', 3, 1, False, 25),
    ('IT3-IOT',   'Internet of Things',                            'IT', 3, 2, False, 27),
    ('IT3-SDN',   'Redes Definidas por Software',                  'IT', 3, 2, False, 25),
    ('IT3-CLOUD', 'Cloud Computing',                               'IT', 3, 2, False, 26),
    ('IT3-GPROJ', 'Gestión de Proyectos Telemáticos',              'IT', 3, 2, False, 24),
    ('IT3-CSEG2', 'Ciberseguridad II',                             'IT', 3, 2, False, 23),

    # ══ DG – 3º ══════════════════════════════════════════════════════════════
    ('DG3-ASO',   'Administración de Sistemas Operativos',         'DG', 3, 1, False, 18),
    ('DG3-GPS',   'Gestión de Proyectos Software',                 'DG', 3, 1, False, 18),
    ('DG3-IA',    'Introducción a la IA',                          'DG', 3, 1, False, 18),
    ('DG3-SDIST', 'Sistemas Distribuidos',                         'DG', 3, 1, False, 18),
    ('DG3-MSIM',  'Modelado y Simulación Robótica',                'DG', 3, 1, False, 18),
    ('DG3-EMBOT', 'Sistemas Empotrados en Tiempo Real',            'DG', 3, 1, False, 18),
    ('DG3-BDA',   'Bases de Datos Avanzadas',                      'DG', 3, 2, False, 18),
    ('DG3-FAA',   'Fundamentos de Aprendizaje Automático',         'DG', 3, 2, False, 18),
    ('DG3-RMOV',  'Robótica Móvil',                                'DG', 3, 2, False, 18),
    ('DG3-RIND',  'Robótica Industrial',                           'DG', 3, 2, False, 18),
    ('DG3-DSA',   'Desarrollo de Software Avanzado',               'DG', 3, 2, False, 18),
    ('DG3-PLAN',  'Planificación Robótica Cognitiva',              'DG', 3, 2, False, 18),

    # ══ II – 4º (solo tarde) ══════════════════════════════════════════════════
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
    ('II4-SSF',   'Diseño de Software Seguro y Fiable',            'II', 4, 2, False, 18),
    ('II4-CIBER', 'Ciberseguridad en Redes y Aplicaciones',        'II', 4, 2, False, 17),

    # ══ IR – 4º (solo tarde) ══════════════════════════════════════════════════
    ('IR4-A1',  'Asignatura 4º IR 1',  'IR', 4, 1, False, 20),
    ('IR4-A2',  'Asignatura 4º IR 2',  'IR', 4, 1, False, 20),
    ('IR4-A3',  'Asignatura 4º IR 3',  'IR', 4, 1, False, 20),
    ('IR4-A4',  'Asignatura 4º IR 4',  'IR', 4, 1, False, 20),
    ('IR4-A5',  'Asignatura 4º IR 5',  'IR', 4, 1, False, 20),
    ('IR4-A6',  'Asignatura 4º IR 6',  'IR', 4, 2, False, 20),
    ('IR4-A7',  'Asignatura 4º IR 7',  'IR', 4, 2, False, 20),
    ('IR4-A8',  'Asignatura 4º IR 8',  'IR', 4, 2, False, 20),
    ('IR4-A9',  'Asignatura 4º IR 9',  'IR', 4, 2, False, 20),
    ('IR4-A10', 'Asignatura 4º IR 10', 'IR', 4, 2, False, 20),

    # ══ IT – 4º (solo tarde) ══════════════════════════════════════════════════
    ('IT4-5G',    'Redes 5G y Tecnologías Emergentes',             'IT', 4, 1, False, 22),
    ('IT4-SECAMP','Seguridad Avanzada y Ciberdefensa',             'IT', 4, 1, False, 21),
    ('IT4-VIRT',  'Virtualización y NFV',                          'IT', 4, 1, False, 20),
    ('IT4-IOT2',  'IoT Avanzado e Industria 4.0',                  'IT', 4, 1, False, 19),
    ('IT4-TFG1',  'Trabajo Fin de Grado I',                        'IT', 4, 1, False, 22),
    ('IT4-BIGDAT','Big Data en Redes',                             'IT', 4, 2, False, 20),
    ('IT4-MOBL',  'Redes Móviles Avanzadas',                       'IT', 4, 2, False, 19),
    ('IT4-SECNUB','Seguridad en la Nube',                          'IT', 4, 2, False, 18),
    ('IT4-PROTEL','Proyectos Telemáticos',                         'IT', 4, 2, False, 21),
    ('IT4-TFG2',  'Trabajo Fin de Grado II',                       'IT', 4, 2, False, 22),

    # ══ DG – 4º (mañana) ══════════════════════════════════════════════════════
    ('DG4-ARQ',   'Arquitectura Software',                         'DG', 4, 1, False, 16),
    ('DG4-IAPP',  'Integración de Aplicaciones',                   'DG', 4, 1, False, 16),
    ('DG4-MULT',  'Desarrollo Multiplataforma',                    'DG', 4, 1, False, 16),
    ('DG4-IRC',   'Ingeniería de Requisitos y Calidad',            'DG', 4, 1, False, 16),
    ('DG4-GPS2',  'Gestión Avanzada de Proyectos',                 'DG', 4, 1, False, 16),
    ('DG4-SPEC1', 'Especialización en Robótica I',                 'DG', 4, 1, False, 16),
    ('DG4-SSF',   'Diseño de Software Seguro y Fiable',            'DG', 4, 2, False, 16),
    ('DG4-CIBER', 'Ciberseguridad en Redes',                       'DG', 4, 2, False, 16),
    ('DG4-DSIS',  'Desarrollo de Software de Sistemas',            'DG', 4, 2, False, 16),
    ('DG4-GPI',   'Gestión de Procesos e Infraestructura',         'DG', 4, 2, False, 16),
    ('DG4-FAA2',  'Aprendizaje Automático Avanzado',               'DG', 4, 2, False, 16),
    ('DG4-SPEC2', 'Especialización en Robótica II',                'DG', 4, 2, False, 16),

    # ══ DG – 5º (híbrido: mañana y tarde) ═════════════════════════════════════
    ('DG5-TFG1',  'Trabajo Fin de Grado I',                        'DG', 5, 1, False, 14),
    ('DG5-PROY1', 'Proyectos de Ingeniería I',                     'DG', 5, 1, False, 14),
    ('DG5-SPEC3', 'Especialización Avanzada I',                    'DG', 5, 1, False, 14),
    ('DG5-SPEC4', 'Especialización Avanzada II',                   'DG', 5, 1, False, 14),
    ('DG5-SPEC5', 'Especialización Avanzada III',                  'DG', 5, 1, False, 14),
    ('DG5-SPEC6', 'Especialización Avanzada IV',                   'DG', 5, 1, False, 14),
    ('DG5-TFG2',  'Trabajo Fin de Grado II',                       'DG', 5, 2, False, 14),
    ('DG5-PROY2', 'Proyectos de Ingeniería II',                    'DG', 5, 2, False, 14),
    ('DG5-SPEC7', 'Especialización Avanzada V',                    'DG', 5, 2, False, 14),
    ('DG5-SPEC8', 'Especialización Avanzada VI',                   'DG', 5, 2, False, 14),
    ('DG5-SPEC9', 'Especialización Avanzada VII',                  'DG', 5, 2, False, 14),
    ('DG5-PRACT', 'Prácticas Externas',                            'DG', 5, 2, False, 14),
]

# ── Vínculos asignaturas compartidas ─────────────────────────────────────────
# (codigo_asignatura_en_II, titulacion_extra_que_la_comparte)
COMPARTIDAS = [
    # II → IR (1º S1)
    ('FPROG', 'IR'), ('FGES', 'IR'), ('TCOM', 'IR'),
    # II → IR (1º S2)
    ('PROG', 'IR'), ('ALIN', 'IR'), ('ECOM', 'IR'), ('FSO', 'IR'), ('CMN', 'IR'),
    # II → IT (1º S1)
    ('FPROG', 'IT'), ('TCOM', 'IT'),
    # II → IT (1º S2)
    ('PROG', 'IT'), ('CMN', 'IT'),
    # II → DG (1º S1)
    ('FPROG', 'DG'), ('FGES', 'DG'), ('TCOM', 'DG'),
    # II → DG (1º S2)
    ('PROG', 'DG'), ('ALIN', 'DG'), ('ECOM', 'DG'), ('FSO', 'DG'),
]

# Asignaturas antiguas (II-TI / II-IS) a eliminar
_CODIGOS_OBSOLETOS = [
    'IITI-FE', 'IITI-DMN', 'IITI-CVE', 'IITI-DA', 'IITI-DAM',
    'IIIS-IAPP', 'IIIS-SDN', 'IIIS-BD', 'IIIS-MULT', 'IIIS-ARQ',
]
_TITULACIONES_OBSOLETAS = ['II-TI', 'II-IS']


class Command(BaseCommand):
    help = 'Pobla/actualiza la BD con el catálogo II, IR, IT y DG (2025-26)'

    def handle(self, *args, **kwargs):
        self._cleanup()
        self._seed_bloques()
        self._seed_titulaciones()
        self._seed_cursos()
        self._seed_asignaturas()
        self._seed_compartidas()
        self.stdout.write('\n\033[92m✅  Seed completado.\033[0m\n')

    def _cleanup(self):
        self.stdout.write('\n─── Limpieza ───')
        n = Asignatura.objects.filter(codigo__in=_CODIGOS_OBSOLETOS).delete()[0]
        self.stdout.write(f'  Asignaturas obsoletas eliminadas: {n}')
        for cod in _TITULACIONES_OBSOLETAS:
            deleted, _ = Titulacion.objects.filter(codigo=cod).delete()
            if deleted:
                self.stdout.write(f'  Titulación eliminada: {cod}')

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
            self.stdout.write(f'  {"✓" if created else "·"} {nombre}  {ini:%H:%M}–{fin:%H:%M}  ({turno})')

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

    def _seed_cursos(self):
        self.stdout.write('\n─── Cursos ───')
        for tit_cod, num, es_ultimo, es_hibrido in CURSOS:
            tit = Titulacion.objects.get(codigo=tit_cod)
            obj, created = Curso.objects.get_or_create(
                titulacion=tit, numero=num,
                defaults=dict(es_ultimo=es_ultimo, es_hibrido=es_hibrido)
            )
            if not created:
                changed = False
                if obj.es_ultimo != es_ultimo:
                    obj.es_ultimo = es_ultimo
                    changed = True
                if obj.es_hibrido != es_hibrido:
                    obj.es_hibrido = es_hibrido
                    changed = True
                if changed:
                    obj.save()
            self.stdout.write(
                f'  {"✓" if created else "·"} {tit_cod} {num}º'
                f'  (tarde={es_ultimo}, híbrido={es_hibrido})'
            )

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
            self.stdout.write(f'    {"✓" if created else "·"} {codigo:<16} S{semestre}  {nombre}')

    def _seed_compartidas(self):
        self.stdout.write('\n─── Vínculos compartidas ───')
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
            except Titulacion.DoesNotExist:
                self.stdout.write(self.style.WARNING(f'  ⚠ Titulación no encontrada: {tit_extra_cod}'))
