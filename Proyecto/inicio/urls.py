from django.urls import path, include
from . import views

urlpatterns = [
  
    path('', views.inicio_view, name='Inicio'),
    path('', views.inicio_view, name='Profesor'),
    path('proyeccion', views.proyeccion_view, name='Proyeccion'),
    path('asignatura', views.asignatura_view, name='Asignatura'),
    path('usuarios', views.usuarios_view, name='Usuarios'),
    path('logout', views.logout_view, name='Logout'),
    path('registro/', views.registro_view, name='Registro'),
    path('coordinador/', views.coordinador_view, name='Coordinador'),
    path('<str:email>/', views.desactivar_usuario, name='desactivar_usuario'),
    path('editar_usuario', views.edit_user, name='EditarUsuario'),
    path('activardesactivar', views.activarusuarios_view, name='ActivarDesactivar'),
    path('cargar', views.cargar_usuarios, name='Cargar'),
    path('proyeccion', views.proyeccion_view, name='Proyeccion'),
    path('enviar-mensaje', views.enviar_mensaje, name='enviar_mensaje'),
    path('buzon-mensajes', views.buzon_mensajes, name='buzon_mensajes'),
    path('export/proyeccion/excel/', views.descargar_tabla, name='descargar_tabla'),
    path('reporte', views.reporte_view, name='Reporte'),
    path('editar', views.proyeccion_list, name='lista'),
    path('proyecciones/<int:id>/editar/', views.editar_proyeccion, name='editar_proyeccion'),
    path('disponibilidad', views.vista_para_profesor, name='registrar_disponibilidad'),
    path('tablaDisponibilidad', views.disponibilidad, name='disponibilidad'),
    path('programacion', views.crear_programacion, name='programacion_nuevo'),
    path('verProgramacion', views.ver_programacion, name='ver_programacion'),
    path('restringir-fechas', views.restringir_fechas, name='restringir_fechas'),
    path('ver-restricciones-fechas', views.ver_restricciones_fechas, name='ver_restricciones_fechas'),
    path('quitar-restricciones', views.quitar_restricciones, name='quitar_restricciones'),


  
    
    
    
    
]