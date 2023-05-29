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
    path('ver-restricciones-fechas', views.ver_restricciones, name='ver_restricciones_fechas'),
    path('seleccionar-fechas', views.restringir, name='seleccionar_fechas'),
    path('cargar_tabla', views.cargar_tabla, name='cargar_tabla'),
    path('disponibilidad/<int:disponibilidad_id>>/editar/', views.editar_disponibilidad, name='editar_disponibilidad'),
    path('editarDisponibilidad', views.vereditdisponibilidad, name='editarDisponibilidad'),
    path('activar_disponibilidad/<int:disponibilidad_id>/', views.activar_disponibilidad, name='activar_disponibilidad'),
    path('desactivar_disponibilidad/<int:disponibilidad_id>/', views.desactivar_disponibilidad, name='desactivar_disponibilidad'),
    path('verprogramacion', views.mostrar_programacion, name='mostrar_programacion'),
    path('mostrar_cronograma', views.mostrar_cronograma, name='mostrar_cronograma'),
    path('llenar-cronograma', views.llenar_cronograma, name='llenar_cronograma'),
    path('cronograma', views.mostrar_cronograma_a_profesor, name='mostrar_cronogramaProfesor'),
    path('cronograma/editar/<int:cronograma_id>/', views.editar_cronograma, name='editar_cronograma'),
    path('cronogramaedit/editar/<int:cronograma_id>/', views.editar_cronograma1, name='editarCronograma'),
    path('activar/<int:cronograma_id>/', views.activar_cronograma, name='activar_cronograma'),
    path('desactivar/<int:cronograma_id>/', views.desactivar_cronograma, name='desactivar_cronograma'),


  
    
    
    
    
]