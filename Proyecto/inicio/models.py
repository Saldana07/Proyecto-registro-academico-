from django.db import models
from django.contrib.auth.models import User
#from django.contrib.auth.models import AbstractUser
# Create your models here.




class Programas(models.Model):
    codigo = models.AutoField(primary_key=True)
    cod = models.CharField(max_length=200)
    nombre = models.CharField(max_length=200)
    correo = models.CharField(max_length=200)
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
        ('LUNES', 'Lunes'),
        ('MARTES', 'Martes'),
        ('MIERCOLES', 'Miércoles'),
        ('JUEVES', 'Jueves'),
        ('VIERNES', 'Viernes'),
        ('SABADO', 'Sábado'),
        ('DOMINGO', 'Domingo'),
    ]
    fecha = models.CharField(choices=DAY_CHOICES, max_length=15)
    hora_inicio = models.CharField(choices=[
        ('07:00', '07:00 AM'),
        ('10:00', '10:00 AM'),
        ('14:00', '02:00 PM'),
        ('17:00', '05:00 PM'),
        ('18:30', '06:30 PM'),
    ], max_length=5)
    hora_fin = models.CharField(choices=[
        ('10:00', '10:00 AM'),
        ('13:00', '01:00 PM'),
        ('17:00', '05:00 PM'),
        ('18:30', '06:30 PM'),
        ('21:30', '09:30 PM'),
    ], max_length=5)
    comentarios = models.TextField(default="Disponible", null=True)
    profesor = models.ForeignKey(User, on_delete=models.CASCADE)
    mostrar_en_tabla = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.profesor.username} - {self.get_fecha_display()} ({self.hora_inicio} - {self.hora_fin})"




    
    
    
class Restriccion(models.Model):
    fecha_inicio = models.DateField()
    fecha_fin = models.DateField()



class Programacion(models.Model):
    id = models.AutoField(primary_key=True)
    programa_jornada = models.CharField(max_length=100)
    codigo_asignatura = models.CharField(max_length=20)
    grupo = models.CharField(max_length=10)
    codigo_grupo = models.CharField(max_length=20)
    cupo = models.IntegerField()
    cupo_generico = models.IntegerField()
    id_usuarios = models.ForeignKey(User, on_delete=models.CASCADE)

    
    def __str__(self):
        return f"{self.codigo_asignatura} - {self.grupo}"
    
    
class Cronograma(models.Model):
    id = models.AutoField(primary_key=True)  # Campo de ID autoincremental
    id_usuarios = models.ForeignKey(User, on_delete=models.CASCADE)
    semana = models.IntegerField()
    fecha =  models.DateTimeField(auto_now_add=True)
    contenido_tematico = models.TextField()
    material_apoyo = models.TextField()
    observaciones = models.TextField()
    chequeo = models.BooleanField(default=False)

    def __str__(self):
        return f"Semana {self.semana}"