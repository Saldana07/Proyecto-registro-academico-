"""
URL configuration for Proyecto project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from inicio.views import login_view,profesor_view,coordinador_view


urlpatterns = [
    path('admin/', admin.site.urls),
    path('inicio/', include('inicio.urls')),
   #path('login/', login_view, name='Login'),
    path('', login_view, name='Login'),
    path('profesor/', profesor_view, name='Profesor'),
    path('coordinador/', coordinador_view, name='Coordinador'),
    
    
 
]

urlpatterns+=static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)