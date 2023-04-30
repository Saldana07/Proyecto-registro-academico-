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
    path('activardesactivar', views.activarusuarios_view, name='ActivarDesactivar'),
    path('cargar_usuarios/', views.cargar_usuarios, name='cargar_usuarios'),
    
 
    
    
    
    
    
]