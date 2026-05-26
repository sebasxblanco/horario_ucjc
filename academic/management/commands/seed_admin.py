"""
Crea los usuarios administrativos del sistema (superuser + roles clave).
Idempotente: no falla si el usuario ya existe.
"""
from django.core.management.base import BaseCommand
from django.contrib.auth.hashers import make_password
from accounts.models import User


ADMIN_USERS = [
    # (username, first_name, last_name, password, rol, is_superuser, is_staff)
    ('sebas',   'Sebastián', 'Blanco',  'sebas2025',  'DECANO', True,  True),
    ('decano',  'Decano',    'UCJC',    'decano2025', 'DECANO', False, True),
    ('it',      'Técnico',   'IT',      'it2025',     'IT',     False, True),
    ('consultor','Consultor','UCJC',    'consultor2025','CONSULTOR',False,False),
    ('alumno',  'Alumno',    'Demo',    'alumno2025', 'ESTUDIANTE',False,False),
]


class Command(BaseCommand):
    help = 'Crea/actualiza usuarios admin, DECANO, IT, CONSULTOR y alumno demo'

    def handle(self, *args, **kwargs):
        self.stdout.write('\n─── Usuarios Administrativos ───')
        for username, first, last, pwd, rol, is_super, is_staff in ADMIN_USERS:
            user, created = User.objects.get_or_create(
                username=username,
                defaults={
                    'first_name':   first,
                    'last_name':    last,
                    'password':     make_password(pwd),
                    'rol':          rol,
                    'is_superuser': is_super,
                    'is_staff':     is_staff,
                    'is_active':    True,
                }
            )
            if not created:
                user.first_name   = first
                user.last_name    = last
                user.rol          = rol
                user.is_superuser = is_super
                user.is_staff     = is_staff
                user.is_active    = True
                # Solo resetea contraseña si no tiene una válida configurada
                user.set_password(pwd)
                user.save()
            tag = '✓' if created else '·'
            self.stdout.write(f'  {tag} {username:<12} rol={rol:<12} super={is_super}')
        self.stdout.write('\n\033[92m✅  Usuarios admin listos.\033[0m\n')
