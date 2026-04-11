from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    """
    Usuario personalizado del sistema de gestión de horarios UCJC.
    Extiende AbstractUser añadiendo un rol para control de acceso (RBAC).
    """

    class Rol(models.TextChoices):
        DECANO     = 'DECANO',     'Decano / Dirección Académica'
        PROFESOR   = 'PROFESOR',   'Profesor'
        ESTUDIANTE = 'ESTUDIANTE', 'Estudiante'
        IT         = 'IT',         'Departamento IT'
        CONSULTOR  = 'CONSULTOR',  'Consultor'

    rol = models.CharField(
        max_length=20,
        choices=Rol.choices,
        default=Rol.ESTUDIANTE,
        verbose_name='Rol'
    )

    class Meta:
        verbose_name = 'Usuario'
        verbose_name_plural = 'Usuarios'

    def __str__(self):
        return f'{self.get_full_name()} ({self.get_rol_display()})'

    def es_decano(self):
        return self.rol == self.Rol.DECANO

    def es_profesor(self):
        return self.rol == self.Rol.PROFESOR

    def es_estudiante(self):
        return self.rol == self.Rol.ESTUDIANTE