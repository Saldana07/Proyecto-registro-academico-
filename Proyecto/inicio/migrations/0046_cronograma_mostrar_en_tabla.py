# Generated by Django 4.2 on 2023-05-29 03:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('inicio', '0045_alter_cronograma_fecha'),
    ]

    operations = [
        migrations.AddField(
            model_name='cronograma',
            name='mostrar_en_tabla',
            field=models.BooleanField(default=True),
        ),
    ]