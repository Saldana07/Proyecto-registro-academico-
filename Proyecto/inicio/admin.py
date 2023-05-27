
from django.contrib import admin

from .models import Proyeccion,Asignatura,Programas,Mensaje,Disponibilidad,Restriccion,Programacion,Cronograma

#from django.contrib.auth.models import User, Group

# Register your models here.

#admin.site.register(User)

class AsignaturaAdmin(admin.ModelAdmin):
    list_display = ('codigo','nombre', 'creditos','intensidad')

admin.site.register(Asignatura, AsignaturaAdmin)

class ProgramasAdmin(admin.ModelAdmin):
    list_display = ('codigo','cod', 'nombre', 'correo', 'jornada')


admin.site.register(Programas, ProgramasAdmin)

class ProyeccionAdmin(admin.ModelAdmin):
    list_display = ('id', 'programa', 'asignatura')
    
    def programa(self, obj):
        return obj.id_programas.nombre
    
    def asignatura(self, obj):
        return obj.id_asignatura.nombre
    
    programa.admin_order_field = 'id_programas__nombre'
    asignatura.admin_order_field = 'id_asignatura__nombre'
admin.site.register(Proyeccion, ProyeccionAdmin)


admin.site.register(Mensaje)

class DisponibilidadAdmin(admin.ModelAdmin):
    list_display = ('profesor', 'fecha', 'hora_inicio', 'hora_fin', 'mostrar_en_tabla' )

admin.site.register(Disponibilidad, DisponibilidadAdmin)





class RestriccionAdmin(admin.ModelAdmin):
    list_display = ('id', 'fecha_inicio', 'fecha_fin')
admin.site.register(Restriccion, RestriccionAdmin)


class ProgramacionAdmin(admin.ModelAdmin):
    list_display = ('id', 'programa_jornada', 'codigo_asignatura', 'grupo', 'codigo_grupo', 'cupo', 'cupo_generico','id_usuarios')
admin.site.register(Programacion,ProgramacionAdmin)

class CronogramaAdmin(admin.ModelAdmin):
    list_display = ('id', 'id_usuarios', 'semana', 'fecha', 'contenido_tematico', 'material_apoyo', 'observaciones', 'chequeo')
admin.site.register(Cronograma,CronogramaAdmin)