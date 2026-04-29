from django.db import models
from accounts.models import User
from academic.models import Titulacion, Curso, Asignatura, BloqueHorario


class HorarioGenerado(models.Model):
    """
    Horario completo para una titulación/curso/semestre.
    Workflow RF-04: BORRADOR → REVISION → APROBADO | RECHAZADO
    """
    class Estado(models.TextChoices):
        BORRADOR  = 'BORRADOR',  'Borrador'
        REVISION  = 'REVISION',  'En revisión'
        APROBADO  = 'APROBADO',  'Aprobado'
        RECHAZADO = 'RECHAZADO', 'Rechazado'

    titulacion       = models.ForeignKey(Titulacion, on_delete=models.CASCADE,
                                         related_name='horarios')
    curso            = models.ForeignKey(Curso, on_delete=models.CASCADE,
                                         related_name='horarios')
    semestre         = models.PositiveSmallIntegerField(
                           choices=[(1,'Semestre 1'),(2,'Semestre 2')])
    anio_academico   = models.CharField(max_length=10, default='2024-25')
    estado           = models.CharField(max_length=10, choices=Estado.choices,
                                        default=Estado.BORRADOR)
    generado_por     = models.ForeignKey(User, on_delete=models.SET_NULL,
                                         null=True, related_name='horarios_generados')
    fecha_generacion = models.DateTimeField(auto_now_add=True)
    notas            = models.TextField(blank=True)

    class Meta:
        verbose_name = 'Horario Generado'
        verbose_name_plural = 'Horarios Generados'
        ordering = ['-fecha_generacion']

    def __str__(self):
        return (f'{self.titulacion.codigo} – {self.curso.numero}º '
                f'S{self.semestre} ({self.anio_academico}) [{self.get_estado_display()}]')

    @property
    def es_editable(self):
        return self.estado in (self.Estado.BORRADOR, self.Estado.RECHAZADO)


class SesionHorario(models.Model):
    """
    Slot (día + bloque) de una asignatura dentro de un horario.
    RD-05/RD-08: garantizado por unique_together + validación del algoritmo.
    """
    class DiaSemana(models.IntegerChoices):
        LUNES     = 1, 'Lunes'
        MARTES    = 2, 'Martes'
        MIERCOLES = 3, 'Miércoles'
        JUEVES    = 4, 'Jueves'
        VIERNES   = 5, 'Viernes'

    horario    = models.ForeignKey(HorarioGenerado, on_delete=models.CASCADE,
                                   related_name='sesiones')
    asignatura = models.ForeignKey(Asignatura, on_delete=models.CASCADE,
                                   related_name='sesiones')
    dia        = models.IntegerField(choices=DiaSemana.choices)
    bloque     = models.ForeignKey(BloqueHorario, on_delete=models.CASCADE,
                                   related_name='sesiones')
    aula       = models.CharField(max_length=20, blank=True)

    class Meta:
        verbose_name = 'Sesión de Horario'
        verbose_name_plural = 'Sesiones de Horario'
        ordering = ['dia', 'bloque__hora_inicio']
        unique_together = ('horario', 'dia', 'bloque')

    def __str__(self):
        return (f'{self.get_dia_display()} {self.bloque} → {self.asignatura.codigo}')
