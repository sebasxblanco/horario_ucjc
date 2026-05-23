"""
Crea Users con rol PROFESOR, sus perfiles Profesor y las asignaciones
profesor ↔ asignatura según el cuadro de docencia del curso 2025-26.
"""
from django.core.management.base import BaseCommand
from django.contrib.auth.hashers import make_password
from accounts.models import User
from academic.models import Profesor, AsignacionProfesorAsignatura, Asignatura


# ── Profesores ────────────────────────────────────────────────────────────────
# (username, first_name, last_name, departamento)
PROFESORES = [
    ('rmontufar',   'Rodrigo',         'Montúfar Chaveznava',              'Física e Informática'),
    ('celiag',      'Celia',           'Gutiérrez Cosío',                  'Ingeniería de Software'),
    ('ivansosa',    'Iván',            'Sosa Gómez',                       'Gestión Empresarial'),
    ('dbanos',      'David',           'Baños',                            'Sistemas y Redes'),
    ('jmbanos',     'José Manuel',     'Baños Expósito',                   'Redes y Comunicaciones'),
    ('dmillan',     'Diego',           'Millán Berdasco',                  'Matemáticas'),
    ('ahachad',     'Anas',            'Ahachad',                          'Arquitectura de Computadores'),
    ('gonzalezrd',  'Diego',           'González Rodríguez',               'Lenguajes y Paradigmas'),
    ('mabravoh',    'Miguel Ángel',    'Bravo Hijón',                      'Robótica'),
    ('dsampedro',   'Domingo',         'Sampedro Lirio',                   'Sistemas Operativos'),
    ('dmoncunill',  'David',           'Martín Moncunill',                 'Programación'),
    ('cesarand',    'César',           'Andrés Sánchez',                   'Sistemas Operativos'),
    ('jmorales',    'Javier',          'Morales Escudero',                 'Inteligencia Artificial'),
    ('jsandubete',  'Julio Emilio',    'Sandubete Galán',                  'Estadística'),
    ('jesushm',     'Jesús',           'Hermoso de Mendoza Hernández',     'Desarrollo de Software'),
    ('lazcanoa',    'Ana',             'Lazcano De Rojas',                 'Redes y Sistemas'),
    ('rodriguezm',  'Raúl',            'Rodríguez Mercado',                'Cloud y DevOps'),
    ('gonzalezgl',  'Lino',            'González García',                  'Bases de Datos'),
    ('ladstatter',  'Félix',           'Ladstatter',                       'Programación'),
    ('popiuc',      'María Petronela', 'Popiuc',                           'Ingeniería de Software'),
    ('gayoso',      'Víctor',          'Gayoso Martínez',                  'Sistemas Distribuidos'),
    ('martinezb',   'Javier',          'Martínez Boada',                   'Matemáticas'),
    # Profesores de 4º IR (nombres pendientes de confirmar)
    ('profe1ir4',   'Profesor',        '1 (4º IR)',   'TBD'),
    ('profe2ir4',   'Profesor',        '2 (4º IR)',   'TBD'),
    ('profe3ir4',   'Profesor',        '3 (4º IR)',   'TBD'),
    ('profe4ir4',   'Profesor',        '4 (4º IR)',   'TBD'),
    ('profe5ir4',   'Profesor',        '5 (4º IR)',   'TBD'),
    ('profe6ir4',   'Profesor',        '6 (4º IR)',   'TBD'),
    ('profe7ir4',   'Profesor',        '7 (4º IR)',   'TBD'),
    ('profe8ir4',   'Profesor',        '8 (4º IR)',   'TBD'),
    ('profe9ir4',   'Profesor',        '9 (4º IR)',   'TBD'),
    ('profe10ir4',  'Profesor',        '10 (4º IR)',  'TBD'),
]

# ── Asignaciones profesor → asignaturas ──────────────────────────────────────
# Fuente: cuadro de docencia 2025-26 + PDF de horarios primer semestre
# (username, [codigos_asignatura])
ASIGNACIONES = [
    # ── II / 1º ──────────────────────────────────────────────────────────────
    ('rmontufar',  ['II-FFIN']),             # Fund. Físicos Inform  M9  J9
    ('celiag',     ['FPROG', 'II-TPROG']),   # Fund. Prog L11 X11 · Taller L13 X13
    ('ivansosa',   ['FGES']),                # Fund. Gestión  M11 J11
    ('dbanos',     ['TCOM']),                # Tecnol. Comput  M13 J13

    # ── II / 2º ──────────────────────────────────────────────────────────────
    ('rmontufar',  ['II2-LAC']),             # Lógica Algor Comp  L13 X13
    ('dmillan',    ['II2-MDIS']),            # Matem. Discreta  L9  J9
    ('jsandubete', ['II2-EST']),             # Estadística  L11 M9
    ('jmbanos',    ['II2-REDES']),           # Redes Computadores  M11 X11
    ('ahachad',    ['II2-ARQC']),            # Arq. Computadores  M13 J11

    # ── II / 3º ──────────────────────────────────────────────────────────────
    ('cesarand',   ['II3-ASO']),             # Adm Serv SO  L9  V9
    ('gonzalezrd', ['II3-LPROG']),           # Lenguajes Paradigmas  L11 X11
    ('dbanos',     ['II3-SDIST']),           # Sist. Distribuidos  X9  J11
    ('jmorales',   ['II3-IA']),              # Intro IA  L13 X13
    ('celiag',     ['II3-GPS']),             # Gestión Proyectos SW  J13 V11

    # ── II / 4º — track IS ───────────────────────────────────────────────────
    ('dsampedro',  ['II4-IAPP']),            # Integración Apps  L1530 X1530
    ('jesushm',    ['II4-SDN']),             # Sol. y Despliegue Nube  M1530 J1530
    ('rodriguezm', ['II4-MULT']),            # Desarrollo Multiplataforma  M1730 J1730
    ('jsandubete', ['II4-ARQ']),             # Arquitectura Software  L1730 X1730
    ('cesarand',   ['II4-BD']),              # Desarrollo Servidor y Big Data
    ('jmbanos',    ['II4-SSF']),             # Diseño SW Seguro  V15 V17  (S2)
    ('jesushm',    ['II4-CIBER']),           # Ciberseguridad  M1930 J1930  (S2)

    # ── II / 4º — track TI ───────────────────────────────────────────────────
    ('rodriguezm', ['II4-FE']),              # Desarrollo Front-End  L1530 X1530
    ('cesarand',   ['II4-DMN']),             # Despliegue y Monitorización  M1530 J1530
    ('jesushm',    ['II4-CVE']),             # Contenedores Virt Escal  M1730 J1730
    ('rodriguezm', ['II4-DA']),              # Despliegue y Automatización  L1730 X1730
    ('rodriguezm', ['II4-DAP']),             # Diseño y Despliegue Apps  L1930 X1930

    # ── IR / 1º ──────────────────────────────────────────────────────────────
    ('rmontufar',  ['IR-FFIS']),             # Fund. Físicos  M11 J11
    ('mabravoh',   ['IR-FIROB']),            # Física para Robótica  L9  X9

    # ── IR / 2º ──────────────────────────────────────────────────────────────
    ('jsandubete', ['IR2-EST']),             # Estadística  L13 M11
    ('mabravoh',   ['IR2-SENS']),            # Sensores y Actuadores  L11 X11
    ('cesarand',   ['IR2-AUTOM']),           # Fund. Automática  M9  X9
    ('jmbanos',    ['IR2-REDES', 'IR2-SENYAL']),  # Redes M13 J13 · Señales X13 J11

    # ── IR / 3º ──────────────────────────────────────────────────────────────
    ('dbanos',     ['IR3-SDIST']),           # Sist. Distribuidos  L9  M11
    ('mabravoh',   ['IR3-MSIM']),            # Modelado y Sim. Rob.  M9  V9
    ('dsampedro',  ['IR3-ASO']),             # Adm Serv SO  L11 X11
    ('mabravoh',   ['IR3-EMBOT']),           # Sist. Empotrados  J13 V11
    ('jmorales',   ['IR3-IA']),              # Intro IA  M13 V13

    # ── IR / 4º ──────────────────────────────────────────────────────────────
    ('profe1ir4',  ['IR4-A1']),
    ('profe2ir4',  ['IR4-A2']),
    ('profe3ir4',  ['IR4-A3']),
    ('profe4ir4',  ['IR4-A4']),
    ('profe5ir4',  ['IR4-A5']),
    ('profe6ir4',  ['IR4-A6']),
    ('profe7ir4',  ['IR4-A7']),
    ('profe8ir4',  ['IR4-A8']),
    ('profe9ir4',  ['IR4-A9']),
    ('profe10ir4', ['IR4-A10']),
]


class Command(BaseCommand):
    help = 'Crea usuarios PROFESOR, perfiles y asignaciones a asignaturas (2025-26)'

    def handle(self, *args, **kwargs):
        perfil_map = self._seed_profesores()
        self._seed_asignaciones(perfil_map)
        self.stdout.write('\n\033[92m✅  Profesores y asignaciones completados.\033[0m\n')

    # ── Crear usuarios y perfiles ─────────────────────────────────────────────
    def _seed_profesores(self):
        self.stdout.write('\n─── Profesores ───')
        perfil_map = {}
        for username, first_name, last_name, depto in PROFESORES:
            user, u_created = User.objects.get_or_create(
                username=username,
                defaults={
                    'first_name': first_name,
                    'last_name':  last_name,
                    'rol':        'PROFESOR',
                    'password':   make_password(f'{username}2025'),
                    'is_active':  True,
                }
            )
            if not u_created:
                user.first_name = first_name
                user.last_name  = last_name
                user.rol        = 'PROFESOR'
                user.save()

            perfil, p_created = Profesor.objects.get_or_create(
                user=user, defaults={'departamento': depto}
            )
            if not p_created and perfil.departamento != depto:
                perfil.departamento = depto
                perfil.save()

            perfil_map[username] = perfil
            tag = '✓' if u_created else '·'
            self.stdout.write(
                f'  {tag} {username:<14} {first_name} {last_name}'
            )
        return perfil_map

    # ── Crear asignaciones ────────────────────────────────────────────────────
    def _seed_asignaciones(self, perfil_map):
        self.stdout.write('\n─── Asignaciones ───')
        for username, codigos in ASIGNACIONES:
            perfil = perfil_map.get(username)
            if not perfil:
                self.stdout.write(self.style.WARNING(f'  ⚠ Perfil no encontrado: {username}'))
                continue
            for codigo in codigos:
                try:
                    asig = Asignatura.objects.get(codigo=codigo)
                except Asignatura.DoesNotExist:
                    self.stdout.write(self.style.WARNING(f'  ⚠ Asignatura no encontrada: {codigo}'))
                    continue
                asignacion, created = AsignacionProfesorAsignatura.objects.update_or_create(
                    asignatura=asig,
                    defaults={'profesor': perfil}
                )
                nombre_corto = perfil.user.get_full_name()
                tag = '✓' if created else '·'
                self.stdout.write(
                    f'  {tag} {codigo:<14} → {nombre_corto}'
                )
