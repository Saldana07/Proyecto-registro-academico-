from django.db import models
from django.contrib.auth.models import User
#from django.contrib.auth.models import AbstractUser
# Create your models here.




class Programas(models.Model):
    codigo = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=200)
    correo = models.CharField(max_length=200)
    id_usuarios = models.ForeignKey(User, on_delete=models.CASCADE)
    jornada = models.CharField(max_length=200)
    def __str__(self):
        return self.nombre
    
class Asignatura(models.Model):
    id = models.AutoField(primary_key=True)
    codigo= models.CharField(max_length=200)
    nombre = models.CharField(max_length=200)
    creditos = models.IntegerField()
    intensidad = models.IntegerField()
    
    def __str__(self):
        return self.nombre
    
    
class Proyeccion(models.Model):
    id = models.AutoField(primary_key=True)
    id_programas = models.ForeignKey(Programas, on_delete=models.CASCADE)
    id_asignatura = models.ForeignKey(Asignatura, on_delete=models.CASCADE, null=True)
    total_semana = models.IntegerField(default=19)
    num_profesores = models.IntegerField(default=1)
    semestre = models.IntegerField(default=1)
    def __str__(self):
        return f"{self.id} ({self.id_programas.nombre}, {self.id_asignatura.nombre})"
    
    
    
class Mensaje(models.Model):
    emisor = models.ForeignKey(User, related_name='mensajes_enviados', on_delete=models.CASCADE)
    receptor = models.ForeignKey(User, related_name='mensajes_recibidos', on_delete=models.CASCADE)
    contenido = models.TextField()
    archivo_adjunto = models.FileField(upload_to='archivos_adjuntos/', blank=True, null=True)
    fecha_envio = models.DateTimeField(auto_now_add=True)
    
"""
class Disponibilidad(models.Model):
    fecha = models.DateField()
    hora_inicio = models.TimeField()
    hora_fin = models.TimeField()
    comentarios = models.TextField()
    profesor = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.profesor.username} - {self.fecha} ({self.hora_inicio}-{self.hora_fin})"
"""
class Disponibilidad(models.Model):
    DAY_CHOICES = [
        ('L', 'Lunes'),
        ('M', 'Martes'),
        ('X', 'Miércoles'),
        ('J', 'Jueves'),
        ('V', 'Viernes'),
        ('S', 'Sábado'),
        ('D', 'Domingo'),
    ]
    fecha = models.CharField(choices=DAY_CHOICES, max_length=1)
    hora_inicio = models.TimeField()
    hora_fin = models.TimeField()
    comentarios = models.TextField(default="Disponible", null=True)
    profesor = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.profesor.username} - {self.get_fecha_display()} ({self.hora_inicio}-{self.hora_fin})"

from django.contrib.auth.models import Group

class Programacion(models.Model):
    DAY_CHOICES1 = [
        ('LUNES', 'Lunes'),
        ('MARTES', 'Martes'),
        ('MIERCOLES', 'Miércoles'),
        ('JUEVES', 'Jueves'),
        ('VIERNES', 'Viernes'),
        ('SABADO', 'Sábado'),
        ('DOMINGO', 'Domingo'),
    ]
    id = models.AutoField(primary_key=True)
    id_proyeccion = models.ForeignKey(Proyeccion, on_delete=models.CASCADE)
    hora = models.TimeField()
    dia = models.CharField(choices=DAY_CHOICES1, max_length=15)

    def __str__(self):
        return f"{self.id_proyeccion.id} ({self.hora}, {self.get_dia_display()})"
    
    
    
class Restriccion(models.Model):
    fecha_inicio = models.DateField()
    fecha_fin = models.DateField()
