# Generated by Django 4.2 on 2023-05-06 05:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('inicio', '0011_remove_mensaje_leido_mensaje_archivo_adjunto'),
    ]

    operations = [
        migrations.AddField(
            model_name='proyeccion',
            name='num_profesores',
            field=models.IntegerField(default=1),
        ),
        migrations.AddField(
            model_name='proyeccion',
            name='total_semana',
            field=models.IntegerField(default=19),
        ),
    ]
