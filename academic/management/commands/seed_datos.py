"""
Pobla la BD con:
  - 4 BloqueHorario (mañana x2 + tarde x2)
  - Asignaturas de 1º II y 1º IR (con AsignaturaCompartida donde corresponda)
"""
from django.core.management.base import BaseCommand
from academic.models import (
    Titulacion, Curso, Asignatura, AsignaturaCompartida, BloqueHorario
)
from datetime import time


# ── Bloques horarios ────────────────────────────────────────────────────────
BLOQUES = [
    ('B1', time(8, 0),  time(10, 0), 'MANANA'),
    ('B2', time(10, 0), time(12, 0), 'MANANA'),
    ('B3', time(15, 0), time(17, 0), 'TARDE'),
    ('B4', time(17, 0), time(19, 0), 'TARDE'),
]

# ── Asignaturas ─────────────────────────────────────────────────────────────
# (codigo, nombre, semestre, solo_II, solo_IR, compartida_con_IR)
# compartida=True  → existe en ambas con el mismo slot (RD-10)

ASIGNATURAS_II = [
    # S1
    ('II-FFIN', 'Fundamentos físicos de la informática', 1, False),
    ('FPROG',   'Fundamentos de Programación',           1, True),
    ('FGES',    'Fundamentos de Gestión Empresarial',    1, True),
    ('ALIN',    'Álgebra Lineal',                        1, True),
    ('TCOM',    'Tecnología de Computadores',            1, True),
    # S2
    ('II-TPROG','Taller de Programación',                2, False),
    ('PROG',    'Programación',                          2, True),
    ('ECOM',    'Estructura de Computadores',            2, True),
    ('FSO',     'Fundamentos de Sistemas Operativos',    2, True),
    ('CMN',     'Cálculo y Métodos Numéricos',           2, True),
]

ASIGNATURAS_IR = [
    # S1
    ('IR-FFIS', 'Fundamentos Físicos',                   1, False),
    ('FPROG',   'Fundamentos de Programación',           1, True),   # shared
    ('FGES',    'Fundamentos de Gestión Empresarial',    1, True),   # shared
    ('ALIN',    'Álgebra Lineal',                        1, True),   # shared
    ('TCOM',    'Tecnología de Computadores',            1, True),   # shared
    # S2
    ('IR-FIROB','Física para Robótica',                  2, False),
    ('PROG',    'Programación',                          2, True),   # shared
    ('ECOM',    'Estructura de Computadores',            2, True),   # shared
    ('FSO',     'Fundamentos de Sistemas Operativos',    2, True),   # shared
    ('CMN',     'Cálculo y Métodos Numéricos',           2, True),   # shared
]


class Command(BaseCommand):
    help = 'Pobla BloqueHorario y asignaturas de 1º II/IR'

    def handle(self, *args, **kwargs):
        self._seed_bloques()
        self._seed_asignaturas()

    # ── Bloques ────────────────────────────────────────────────────────────
    def _seed_bloques(self):
        self.stdout.write('\n─── Bloques Horarios ───')
        for nombre, ini, fin, turno in BLOQUES:
            obj, created = BloqueHorario.objects.get_or_create(
                nombre=nombre,
                defaults=dict(hora_inicio=ini, hora_fin=fin, turno=turno, activo=True)
            )
            tag = '✓ CREADO' if created else '· existe'
            self.stdout.write(f'  {tag}  {obj.nombre}  {ini:%H:%M}–{fin:%H:%M}  ({turno})')

    # ── Asignaturas ────────────────────────────────────────────────────────
    def _seed_asignaturas(self):
        self.stdout.write('\n─── Asignaturas ───')

        tit_ii = Titulacion.objects.get(codigo='II')
        tit_ir = Titulacion.objects.get(codigo='IR')
        curso_ii = Curso.objects.get(titulacion=tit_ii, numero=1)
        curso_ir = Curso.objects.get(titulacion=tit_ir, numero=1)

        # Limpia la asignatura de prueba antigua si existe
        Asignatura.objects.filter(codigo='MAT101').update(
            nombre='Álgebra Lineal', codigo='ALIN',
            semestre=1, sesiones_semana=2, horas_sesion=2, es_compartida=True
        )

        shared_map = {}  # codigo → Asignatura object (para vincular compartidas)

        # ── II ──
        self.stdout.write('\n  [II – 1º]')
        for codigo, nombre, sem, compartida in ASIGNATURAS_II:
            obj, created = Asignatura.objects.get_or_create(
                codigo=codigo,
                defaults=dict(
                    nombre=nombre, curso=curso_ii, semestre=sem,
                    horas_sesion=2, sesiones_semana=2, es_compartida=compartida
                )
            )
            if not created:
                # Actualiza por si cambió algo
                obj.nombre = nombre
                obj.curso = curso_ii
                obj.semestre = sem
                obj.es_compartida = compartida
                obj.save()

            if compartida:
                shared_map[codigo] = obj

            tag = '✓' if created else '·'
            self.stdout.write(f'    {tag} {codigo:<12} {nombre}  (S{sem}{"  [COMPARTIDA]" if compartida else ""})')

        # ── IR ──
        self.stdout.write('\n  [IR – 1º]')
        for codigo, nombre, sem, compartida in ASIGNATURAS_IR:
            if compartida and codigo in shared_map:
                # La asignatura ya existe (fue creada para II), solo creamos el vínculo
                asig_ii = shared_map[codigo]
                vinculo, v_created = AsignaturaCompartida.objects.get_or_create(
                    asignatura=asig_ii, titulacion=tit_ir
                )
                tag = '↔ VINCULADA' if v_created else '· ya vinculada'
                self.stdout.write(f'    {tag}  {codigo:<12} {nombre}  (S{sem})')
            else:
                # Asignatura exclusiva de IR
                obj, created = Asignatura.objects.get_or_create(
                    codigo=codigo,
                    defaults=dict(
                        nombre=nombre, curso=curso_ir, semestre=sem,
                        horas_sesion=2, sesiones_semana=2, es_compartida=False
                    )
                )
                if not created:
                    obj.nombre = nombre
                    obj.curso = curso_ir
                    obj.semestre = sem
                    obj.save()
                tag = '✓' if created else '·'
                self.stdout.write(f'    {tag} {codigo:<12} {nombre}  (S{sem})')

        self.stdout.write('\n✅  Seed completado.\n')
