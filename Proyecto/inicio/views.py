from django.http import HttpResponse
from django.shortcuts import render
import openpyxl


from django.contrib.auth.models import User
# Create your views here.
from django.contrib import auth
from django.shortcuts import render, redirect
from django.contrib import auth
from .forms import LoginForm, registro_form,EditUserForm,ProyeccionForm,ProyeccionEditForm
from django.contrib.auth import login, authenticate
from django.contrib.auth.models import Group
from django.shortcuts import render, get_object_or_404
from .models import Proyeccion,Asignatura,Programas,Mensaje
from django.contrib.auth.models import Group, Permission

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
    user= User.objects.all().prefetch_related('grups')
    context = {
        'usuarios':usuarios,
        'user':user,
        
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





def edit_user(request):
    user = request.user
    group = user.groups.first()
    form = EditUserForm(request.POST or None, instance=user,initial={'group': group})
    if form.is_valid():
        form.save()
        return redirect('/inicio/editar_usuario')
    return render(request, 'editarusuario.html', {'form': form})



def desactivar_usuario(request, email):
    
    usuario = get_object_or_404(User, email=email)
    usuario.is_active = not usuario.is_active  # invertir el estado actual
    usuario.save()
    return redirect(request.META.get('HTTP_REFERER', '/'))

from django.contrib.auth.models import Group
def activarusuarios_view(request):
    usuarios= User.objects.all()
    user= User.objects.all().prefetch_related('grups')
    
    context = {
        'usuarios':usuarios,
        'user':user,
        
    }
    return render(request,'activarDesactivar.html',context)


def cargar_usuarios(request):
    if request.method == 'POST' and request.FILES['ejemplo']:
        # Obtener el archivo del formulario
        file = request.FILES['ejemplo']
        # Abrir el archivo con openpyxl
        workbook = openpyxl.load_workbook(file)
        # Seleccionar la hoja que contiene los datos de usuario
        sheet = workbook['Sheet1']
        # Iterar sobre cada fila de la hoja y guardar los datos en la base de datos
        for row in sheet.iter_rows(min_row=2, values_only=True):
            username, email, password, first_name, last_name, group_name = row
            password = str(password) # Convertir la contraseña en una cadena
            # Obtener o crear el usuario
            user, created = User.objects.get_or_create(username=username, email=email)
            user.first_name = first_name
            user.last_name = last_name
            user.set_password(password)
            user.save()
            # Obtener o crear el grupo
            group, created = Group.objects.get_or_create(name=group_name)
            # Agregar al usuario al grupo
            user.groups.add(group)
        # Redirigir a una página de éxito después de guardar los datos
        return render(request, 'cargar.html')
    else:
        # Renderizar el formulario para cargar el archivo si el método no es POST
        return render(request, 'cargar.html')


def enviar_mensaje(request):
    if request.method == 'POST':
        receptor_id = request.POST['receptor']
        receptor = User.objects.get(id=receptor_id)
        contenido = request.POST['contenido']
        archivo_adjunto = request.FILES.get('archivo_adjunto')  # Obtener el archivo adjunto

        mensaje = Mensaje(emisor=request.user, receptor=receptor, contenido=contenido)
        mensaje.archivo_adjunto = archivo_adjunto  # Asignar el archivo adjunto al mensaje
        mensaje.save()

        # Puedes agregar lógica adicional aquí, como notificar al receptor por correo electrónico

    usuarios = User.objects.exclude(id=request.user.id)  # Obtén todos los usuarios excepto el usuario actual
    return render(request, 'enviar_mensaje.html', {'usuarios': usuarios})



def buzon_mensajes(request):
    mensajes_recibidos = Mensaje.objects.filter(receptor=request.user).order_by('-fecha_envio')
    return render(request, 'buzon_mensajes.html', {'mensajes_recibidos': mensajes_recibidos})

def get_datos():
    proyecciones = Proyeccion.objects.select_related('id_programas', 'id_asignatura')
    datos = []

    for proyeccion in proyecciones:
        semestre = proyeccion.id_programas.jornada
        codigo = proyeccion.id_asignatura.codigo
        asignatura = proyeccion.id_asignatura.nombre
        creditos = proyeccion.id_asignatura.creditos
        intensidad = proyeccion.id_asignatura.intensidad
        total_semana = 19  # Aquí podrías definir la cantidad de semanas que desees
        num_profesores = 1  # Aquí podrías definir el número de profesores que desees
        total_a_pagar = intensidad * total_semana * num_profesores

        datos.append({
            'semestre': semestre,
            'codigo': codigo,
            'asignatura': asignatura,
            'creditos': creditos,
            'intensidad': intensidad,
            'total_semana': total_semana,
            'num_profesores': num_profesores,
            'total_a_pagar': total_a_pagar,
        })

    return datos

def proyeccion_view(request):
    if request.method == 'POST':
        form = ProyeccionForm(request.POST)
        if form.is_valid():
            id_programas = form.cleaned_data['id_programas']
            id_asignatura = form.cleaned_data['id_asignatura']
            proyeccion = Proyeccion.objects.create(id_programas=id_programas, id_asignatura=id_asignatura)
            return redirect('/inicio/proyeccion')
    else:
        form = ProyeccionForm()
        reporte_context = reporte_view(request)
        context = {
        'form': form,
        'datos': reporte_context,
        }
     

    return render(request, 'proyeccion.html',context)

def descargar_tabla(request):
    datos = get_datos() # Suponiendo que tienes una función que te devuelve los datos de la tabla
    response = HttpResponse(content_type='application/ms-excel')
    response['Content-Disposition'] = 'attachment; filename="proyeccion.xlsx"'

    workbook = openpyxl.Workbook()
    sheet = workbook.active

    # Agregar encabezados a la hoja de cálculo
    sheet['A1'] = 'Semestre'
    sheet['B1'] = 'Código'
    sheet['C1'] = 'Asignatura'
    sheet['D1'] = 'Créditos'
    sheet['E1'] = 'Intensidad'
    sheet['F1'] = 'Total Semana'
    sheet['G1'] = 'N° Profesores'
    sheet['H1'] = 'Total a Pagar'

    # Agregar datos a la hoja de cálculo
    row = 2
    for dato in datos:
        sheet.cell(row=row, column=1).value = dato['semestre']
        sheet.cell(row=row, column=2).value = dato['codigo']
        sheet.cell(row=row, column=3).value = dato['asignatura']
        sheet.cell(row=row, column=4).value = dato['creditos']
        sheet.cell(row=row, column=5).value = dato['intensidad']
        sheet.cell(row=row, column=6).value = dato['total_semana']
        sheet.cell(row=row, column=7).value = dato['num_profesores']
        sheet.cell(row=row, column=8).value = dato['total_a_pagar']
        row += 1

    workbook.save(response)
    return response


def toggle_permission(request, group_id, permission_name):
    group = Group.objects.get(id=group_id)
    permission = Permission.objects.get(codename=permission_name)

    if 'add' in request.GET:
        group.permissions.add(permission)
    elif 'remove' in request.GET:
        group.permissions.remove(permission)

    return redirect('group_detail', group_id=group.id)



def reporte_view(request):

    proyecciones = Proyeccion.objects.select_related('id_programas', 'id_asignatura')
    datos = []


    total_intensidad = 0
    total_semana = 0
    total_profesores = 0
    total_pago = 0

    for proyeccion in proyecciones:
        semestre = proyeccion.id_programas.jornada
        codigo = proyeccion.id_asignatura.codigo
        asignatura = proyeccion.id_asignatura.nombre
        creditos = proyeccion.id_asignatura.creditos
        intensidad = proyeccion.id_asignatura.intensidad
        total_semana = proyeccion.total_semana
        num_profesores = proyeccion.num_profesores

        datos.append({
            'semestre': semestre,
            'codigo': codigo,
            'asignatura': asignatura,
            'creditos': creditos,
            'intensidad': intensidad,
            'total_semana': total_semana,
            'num_profesores': num_profesores,
            'total_a_pagar': intensidad*total_semana,
        })
        total_intensidad+= intensidad
        total_semana += 19
        total_profesores += 1
        total_pago += intensidad*19

    context = {
    
        'datos': datos,
        'total_intensidad': total_intensidad,
        'total_semana': total_semana,
        'total_profesores': total_profesores,
        'total_pago': total_pago,
    }
   
    return render(request, 'reporte.html', context)    




def proyeccion_edit(request, id):
    proyeccion = get_object_or_404(Proyeccion, id=id)
    if request.method == 'POST':
        form = ProyeccionForm(request.POST, instance=proyeccion)
        if form.is_valid():
            form.save()
            return redirect('/inicio/reporte')
    else:
        form = ProyeccionForm(instance=proyeccion)
    context = {'form': form}
    return render(request, 'editarProyeccion.html', context)

    
