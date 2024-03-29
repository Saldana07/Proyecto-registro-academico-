# Generated by Django 4.2 on 2023-05-25 21:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('inicio', '0027_delete_programacion'),
    ]

    operations = [
        migrations.CreateModel(
            name='Programacion',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('programa_jornada', models.CharField(max_length=100)),
                ('codigo_asignatura', models.CharField(max_length=20)),
                ('grupo', models.CharField(max_length=10)),
                ('codigo_grupo', models.CharField(max_length=20)),
                ('cupo', models.IntegerField()),
                ('cupo_generico', models.IntegerField()),
            ],
        ),
    ]
