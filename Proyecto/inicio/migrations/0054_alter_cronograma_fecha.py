# Generated by Django 4.2 on 2023-06-24 15:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('inicio', '0053_programacion_salon'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cronograma',
            name='fecha',
            field=models.DateField(),
        ),
    ]
