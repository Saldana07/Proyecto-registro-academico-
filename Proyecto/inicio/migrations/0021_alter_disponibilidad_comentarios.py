# Generated by Django 4.2 on 2023-05-13 23:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('inicio', '0020_disponibilidad'),
    ]

    operations = [
        migrations.AlterField(
            model_name='disponibilidad',
            name='comentarios',
            field=models.TextField(default='Disponible'),
        ),
    ]