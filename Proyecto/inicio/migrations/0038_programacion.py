# Generated by Django 4.2 on 2023-05-25 23:38

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('inicio', '0037_delete_programacion'),
    ]

    operations = [
        migrations.CreateModel(
            name='Programacion',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('grupo', models.CharField(max_length=10)),
                ('codigo_grupo', models.CharField(max_length=20)),
                ('cupo', models.IntegerField()),
                ('cupo_generico', models.IntegerField()),
                ('codigo_asignatura', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='inicio.asignatura')),
                ('id_usuarios', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('programa_jornada', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='inicio.programas')),
            ],
        ),
    ]
