# Generated by Django 4.2 on 2023-05-26 17:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('inicio', '0042_programas_cod'),
    ]

    operations = [
        migrations.AlterField(
            model_name='programas',
            name='cod',
            field=models.CharField(max_length=200),
        ),
    ]
