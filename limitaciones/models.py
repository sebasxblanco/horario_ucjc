from django.db import models
from accounts.models import User
from academic.models import Asignatura, BloqueHorario


class Limitacion(models.Model):

    class Tipo(models.TextChoices):
        AUSENCIA    = 'AUSENCIA',    'Ausencia'
        RETRASO     = 'RETRASO',     'Retraso'
        CAMBIO_AULA = 'CAMBIO_AULA', 'Cambio de aula'
        MATERIAL    = 'MATERIAL',    'Falta de material'
        OTRO        = 'OTRO',        'Otro'

    class Estado(models.TextChoices):
        PENDIENTE = 'PENDIENTE', 'Pendiente'
        REVISADA  = 'REVISADA',  'Revisada'
        RESUELTA  = 'RESUELTA',  'Resuelta'
        RECHAZADA = 'RECHAZADA', 'Rechazada'

    profesor         = models.ForeignKey(
        User, on_delete=models.CASCADE,
        related_name='limitaciones_reportadas',
        verbose_name='Profesor'
    )
    asignatura       = models.ForeignKey(
        Asignatura, on_delete=models.SET_NULL,
        null=True, blank=True,
        verbose_name='Asignatura afectada'
    )
    fecha            = models.DateField(verbose_name='Fecha del problema')
    bloque           = models.ForeignKey(
        BloqueHorario, on_delete=models.SET_NULL,
        null=True, blank=True,
        verbose_name='Bloque horario'
    )
    tipo             = models.CharField(
        max_length=15, choices=Tipo.choices,
        default=Tipo.AUSENCIA, verbose_name='Tipo'
    )
    descripcion      = models.TextField(verbose_name='Descripción del problema')
    estado           = models.CharField(
        max_length=15, choices=Estado.choices,
        default=Estado.PENDIENTE, verbose_name='Estado'
    )
    respuesta_decano = models.TextField(
        blank=True, verbose_name='Respuesta del decano'
    )
    creada_en        = models.DateTimeField(auto_now_add=True)
    actualizada_en   = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-creada_en']
        verbose_name = 'Limitación'
        verbose_name_plural = 'Limitaciones'

    def __str__(self):
        return f'{self.get_tipo_display()} — {self.profesor.username} — {self.fecha}'

    @property
    def es_pendiente(self):
        return self.estado == self.Estado.PENDIENTE
