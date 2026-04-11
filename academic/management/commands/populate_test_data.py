"""
Comando de gestión: populate_test_data
Crea 3 asignaturas de prueba distribuidas entre los cursos existentes.

Uso:
    python manage.py populate_test_data
"""
from django.core.management.base import BaseCommand, CommandError
from academic.models import Titulacion, Curso, Asignatura


ASIGNATURAS = [
    # (codigo, nombre, idx_curso, sesiones_semana, horas_sesion, es_compartida)
    # Los índices corresponden al orden de: ORDER BY titulacion__nombre, numero
    # [0]=primera titulación 1º, [1]=primera titulación último curso
    # [2]=segunda titulación 1º, [3]=segunda titulación último curso
    ('INF101', 'Programación I',                0, 3, 2, False),
    ('MAT101', 'Álgebra y Matemática Discreta', 0, 2, 2, False),
    ('ROB101', 'Cinemática de Robots',          2, 2, 2, False),
]


class Command(BaseCommand):
    help = 'Crea 3 asignaturas de prueba en los cursos existentes'

    def handle(self, *args, **options):
        cursos = list(
            Curso.objects.select_related('titulacion')
                         .order_by('titulacion__nombre', 'numero')
        )

        if len(cursos) < 2:
            raise CommandError(
                'Se necesitan al menos 2 cursos en la base de datos. '
                'Créalos primero desde /admin/.'
            )

        self.stdout.write(self.style.HTTP_INFO(
            f'\nCursos disponibles ({len(cursos)}):')
        )
        for i, c in enumerate(cursos):
            self.stdout.write(f'  [{i}] {c}')

        self.stdout.write('')
        creadas = 0

        for codigo, nombre, idx, ses, horas, compartida in ASIGNATURAS:
            curso = cursos[idx]
            asig, created = Asignatura.objects.get_or_create(
                codigo=codigo,
                defaults={
                    'nombre': nombre,
                    'curso': curso,
                    'sesiones_semana': ses,
                    'horas_sesion': horas,
                    'es_compartida': compartida,
                },
            )
            if created:
                creadas += 1
                self.stdout.write(
                    self.style.SUCCESS(
                        f'  + {asig.codigo} — {asig.nombre}  '
                        f'({ses} ses/sem · {horas}h)  →  {curso}'
                    )
                )
            else:
                self.stdout.write(
                    f'  · {asig.codigo} ya existe, sin cambios'
                )

        self.stdout.write('')
        if creadas:
            self.stdout.write(
                self.style.SUCCESS(f'{creadas} asignatura(s) creada(s). ✓')
            )
        else:
            self.stdout.write('Todas las asignaturas ya existían.')
