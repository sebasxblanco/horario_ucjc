from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('academic', '0003_add_matriculados_to_asignatura'),
    ]

    operations = [
        migrations.AddField(
            model_name='curso',
            name='es_hibrido',
            field=models.BooleanField(
                default=False,
                verbose_name='¿Horario híbrido?',
                help_text='Las clases se pueden generar tanto por la mañana como por la tarde (Doble Grado último año)'
            ),
        ),
    ]
