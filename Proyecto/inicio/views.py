from django.http import HttpResponse
from django.shortcuts import render
import openpyxl


from .models import User
# Create your views here.
from django.contrib import auth
from django.shortcuts import render, redirect
from django.contrib import auth
from .forms import LoginForm, registro_form,EditUserForm
from django.contrib.auth import login, authenticate
from django.contrib.auth.models import Group



# Create your views here.
def inicio_view(request):
    return render(request,'base.html')

def profesor_view(request):
    return render(request,'baseProfesor.html')


def coordinador_view(request):
    return render(request,'baseCoordinacion.html')


def proyeccion_view(request):
    return render(request,'proyeccion.html')

def asignatura_view(request):
    return render(request,'asignatura.html')

def desactivar_view(request):
    return render(request,'DesactivarUsuario.html')



def usuarios_view(request):
    usuarios= User.objects.all()
    
    context = {
        'usuarios':usuarios,
        
    }
    return render(request,'usuarios.html',context)





def login_view(request):
    if request.method == 'POST':
        form = LoginForm(data=request.POST)
        if form.is_valid():
            user = auth.authenticate(username=form.cleaned_data.get('username'),
                                      password=form.cleaned_data.get('password'))
            auth.login(request, user)
            return redirect('/inicio/')
  
    else:
        form = LoginForm()
    return render(request, 'login.html', {'form': form})


def logout_view(request):
    return redirect('/')  # Cambia 'login' por la URL de tu página de inicio de sesión

def registro_view(request):
    if request.method == 'POST':
        form = registro_form(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.username = form.cleaned_data['username']
            user.save()
            group = form.cleaned_data.get('group')
            if group:
                group.user_set.add(user)
            
            return redirect('/inicio/registro/')
    else:
        form = registro_form()
    return render(request, 'registro.html', {'form': form})


def editarUsuario_view(request):
    return

 
def desactivate_user(request, user_email):
    user = User.objects.get(email=user_email)
    user.is_active = False
    user.save()
    return redirect('/inicio/registro/')

from django.shortcuts import get_object_or_404
def desactivar_usuario(request, email):
    usuario = get_object_or_404(User, email=email)
    usuario.is_active = not usuario.is_active  # invertir el estado actual
    usuario.save()
    return redirect(request.META.get('HTTP_REFERER', '/'))

from django.contrib.auth.models import Group
def activarusuarios_view(request):
    usuarios= User.objects.all()

    
    context = {
        'usuarios':usuarios,
       
        
    }
    return render(request,'activarDesactivar.html',context)




def cargar_usuarios(request):
    if request.method == 'POST' and request.FILES['xlsfile']:
        # Obtener el archivo del formulario
        file = request.FILES['xlsfile']
        # Abrir el archivo con openpyxl
        workbook = openpyxl.load_workbook(file)
        # Seleccionar la hoja que contiene los datos de usuario
        sheet = workbook['Sheet1']
        # Iterar sobre cada fila de la hoja y guardar los datos en la base de datos
        for row in sheet.iter_rows(min_row=2, values_only=True):
            username, email, password, first_name, last_name = row
            user, created = User.objects.get_or_create(username=username, email=email)
            user.first_name = first_name
            user.last_name = last_name
            user.set_password(password)
            user.save()
        # Redirigir a una página de éxito después de guardar los datos
        return render(request, 'load_users.html')
    else:
        # Renderizar el formulario para cargar el archivo si el método no es POST
        return render(request, 'load_users.html')