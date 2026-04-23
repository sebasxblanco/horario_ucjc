from django.db import models
from accounts.models import User


class Titulacion(models.Model):
    """Titulación universitaria (ej: Ingeniería Informática)."""
    nombre = models.CharField(max_length=100, verbose_name='Nombre')
    codigo = models.CharField(max_length=10, unique=True, verbose_name='Código')
    activa = models.BooleanField(default=True, verbose_name='Activa')

    class Meta:
        verbose_name = 'Titulación'
        verbose_name_plural = 'Titulaciones'
        ordering = ['nombre']

    def __str__(self):
        return self.nombre


class Curso(models.Model):
    """
    Curso académico dentro de una titulación.
    RD-04: si es_ultimo=True, las clases se generan solo por la tarde.
    """
    titulacion = models.ForeignKey(
        Titulacion, on_delete=models.CASCADE,
        related_name='cursos', verbose_name='Titulación'
    )
    numero   = models.PositiveSmallIntegerField(verbose_name='Número de curso')
    es_ultimo = models.BooleanField(
        default=False,
        verbose_name='¿Es último curso?',
        help_text='Las clases de este curso se generan exclusivamente por la tarde (RD-04)'
    )

    class Meta:
        verbose_name = 'Curso'
        verbose_name_plural = 'Cursos'
        unique_together = ('titulacion', 'numero')
        ordering = ['titulacion', 'numero']

    def __str__(self):
        return f'{self.titulacion.codigo} — {self.numero}º curso'


class Asignatura(models.Model):
    """
    Asignatura de un curso.
    RD-01: 2h por sesión. RD-02: 2 sesiones/semana. RD-07: un único profesor.
    """
    nombre          = models.CharField(max_length=150, verbose_name='Nombre')
    codigo          = models.CharField(max_length=15, unique=True, verbose_name='Código')
    curso           = models.ForeignKey(
        Curso, on_delete=models.CASCADE,
        related_name='asignaturas', verbose_name='Curso'
    )
    class Semestre(models.IntegerChoices):
        PRIMERO  = 1, 'Semestre 1'
        SEGUNDO  = 2, 'Semestre 2'

    semestre        = models.IntegerField(
        choices=Semestre.choices, default=Semestre.PRIMERO, verbose_name='Semestre'
    )
    horas_sesion    = models.PositiveSmallIntegerField(default=2, verbose_name='Horas por sesión')
    sesiones_semana = models.PositiveSmallIntegerField(default=2, verbose_name='Sesiones por semana')
    es_compartida   = models.BooleanField(
        default=False,
        verbose_name='¿Compartida entre titulaciones?',
        help_text='RD-10: obliga a bloquear el mismo slot en todas las titulaciones vinculadas'
    )

    class Meta:
        verbose_name = 'Asignatura'
        verbose_name_plural = 'Asignaturas'
        ordering = ['curso', 'nombre']

    def __str__(self):
        return f'{self.codigo} — {self.nombre}'


class AsignaturaCompartida(models.Model):
    """
    Vincula una asignatura con las titulaciones adicionales que la comparten (RD-10).
    """
    asignatura = models.ForeignKey(
        Asignatura, on_delete=models.CASCADE,
        related_name='compartidas', verbose_name='Asignatura'
    )
    titulacion = models.ForeignKey(
        Titulacion, on_delete=models.CASCADE,
        related_name='asignaturas_compartidas', verbose_name='Titulación'
    )

    class Meta:
        verbose_name = 'Asignatura Compartida'
        verbose_name_plural = 'Asignaturas Compartidas'
        unique_together = ('asignatura', 'titulacion')

    def __str__(self):
        return f'{self.asignatura.codigo} ↔ {self.titulacion.codigo}'


class Profesor(models.Model):
    """Perfil de usuario con rol PROFESOR."""
    user         = models.OneToOneField(
        User, on_delete=models.CASCADE,
        related_name='perfil_profesor', verbose_name='Usuario'
    )
    departamento = models.CharField(max_length=100, verbose_name='Departamento')

    class Meta:
        verbose_name = 'Profesor'
        verbose_name_plural = 'Profesores'

    def __str__(self):
        return f'Prof. {self.user.get_full_name()}'


class DisponibilidadProfesor(models.Model):
    """
    Franja de disponibilidad o bloqueo de un profesor.
    RF-06: el profesor gestiona su propia disponibilidad.
    """
    class DiaSemana(models.IntegerChoices):
        LUNES     = 1, 'Lunes'
        MARTES    = 2, 'Martes'
        MIERCOLES = 3, 'Miércoles'
        JUEVES    = 4, 'Jueves'
        VIERNES   = 5, 'Viernes'

    class Tipo(models.TextChoices):
        PREFERENTE = 'PREFERENTE', 'Disponibilidad preferente'
        BLOQUEADO  = 'BLOQUEADO',  'Bloqueo (no disponible)'

    profesor    = models.ForeignKey(
        Profesor, on_delete=models.CASCADE,
        related_name='disponibilidades', verbose_name='Profesor'
    )
    dia         = models.IntegerField(choices=DiaSemana.choices, verbose_name='Día')
    hora_inicio = models.TimeField(verbose_name='Hora de inicio')
    hora_fin    = models.TimeField(verbose_name='Hora de fin')
    tipo        = models.CharField(max_length=15, choices=Tipo.choices,
                                   default=Tipo.PREFERENTE, verbose_name='Tipo')

    class Meta:
        verbose_name = 'Disponibilidad del Profesor'
        verbose_name_plural = 'Disponibilidades de Profesores'

    def __str__(self):
        return (f'{self.profesor} — {self.get_dia_display()} '
                f'{self.hora_inicio:%H:%M}–{self.hora_fin:%H:%M}')


class BloqueHorario(models.Model):
    """
    Franja horaria configurable del sistema (RD-03, RD-04).
    Todo debe ser configurable — RD requisito MUST.
    """
    class Turno(models.TextChoices):
        MANANA = 'MANANA', 'Mañana'
        TARDE  = 'TARDE',  'Tarde'

    nombre      = models.CharField(max_length=30, verbose_name='Nombre del bloque')
    hora_inicio = models.TimeField(verbose_name='Hora de inicio')
    hora_fin    = models.TimeField(verbose_name='Hora de fin')
    turno       = models.CharField(max_length=6, choices=Turno.choices, verbose_name='Turno')
    activo      = models.BooleanField(default=True)

    class Meta:
        verbose_name = 'Bloque Horario'
        verbose_name_plural = 'Bloques Horarios'
        ordering = ['hora_inicio']

    def __str__(self):
        return f'{self.nombre} ({self.hora_inicio:%H:%M}–{self.hora_fin:%H:%M})'


class AsignacionProfesorAsignatura(models.Model):
    """
    Asigna un profesor a una asignatura concreta (RD-07).
    Cada asignatura tiene exactamente un profesor.
    """
    profesor   = models.ForeignKey(
        Profesor, on_delete=models.CASCADE,
        related_name='asignaciones', verbose_name='Profesor'
    )
    asignatura = models.OneToOneField(
        Asignatura, on_delete=models.CASCADE,
        related_name='asignacion', verbose_name='Asignatura'
    )

    class Meta:
        verbose_name = 'Asignación Profesor–Asignatura'
        verbose_name_plural = 'Asignaciones Profesor–Asignatura'

    def __str__(self):
        return f'{self.profesor} → {self.asignatura.codigo}'