# Generated by Django 4.2 on 2023-06-17 18:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('inicio', '0049_asistencia_noasistio'),
    ]

    operations = [
        migrations.AddField(
            model_name='asistencia',
            name='fecha_recuperacion',
            field=models.DateField(blank=True, null=True),
        ),
    ]