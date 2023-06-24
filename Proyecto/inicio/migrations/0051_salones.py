# Generated by Django 4.2 on 2023-06-17 20:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('inicio', '0050_asistencia_fecha_recuperacion'),
    ]

    operations = [
        migrations.CreateModel(
            name='Salones',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('nombre', models.CharField(max_length=300)),
                ('tipo', models.CharField(max_length=300)),
                ('capacidad', models.PositiveIntegerField(default=0)),
            ],
        ),
    ]
