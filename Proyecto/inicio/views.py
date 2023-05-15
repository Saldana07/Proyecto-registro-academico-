from audioop import reverse
from django import forms
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
import openpyxl


from django.contrib.auth.models import User
# Create your views here.
from django.contrib import auth
from django.shortcuts import render, redirect
from django.contrib import auth
from .forms import DisponibilidadForm, LoginForm, registro_form,EditUserForm,ProyeccionForm,ProgramacionForm,RestringirFechasForm
from django.contrib.auth import login, authenticate
from django.shortcuts import render, get_object_or_404
from .models import Disponibilidad, Proyeccion,Asignatura,Programas,Mensaje
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
        semestre = proyeccion.semestre
        jornada = proyeccion.id_programas.jornada
        codigo = proyeccion.id_asignatura.codigo
        asignatura = proyeccion.id_asignatura.nombre
        creditos = proyeccion.id_asignatura.creditos
        intensidad = proyeccion.id_asignatura.intensidad
        total_semana = 19  # Aquí podrías definir la cantidad de semanas que desees
        num_profesores = 1  # Aquí podrías definir el número de profesores que desees
        total_a_pagar = intensidad * total_semana * num_profesores

        datos.append({
            'semestre': semestre,
            'jornada': jornada,
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
            semestre = form.cleaned_data['semestre']
            
            proyeccion = Proyeccion.objects.create(id_programas=id_programas, id_asignatura=id_asignatura,semestre=semestre)
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
    sheet['B1'] = 'Jornada'
    sheet['C1'] = 'Código'
    sheet['D1'] = 'Asignatura'
    sheet['E1'] = 'Créditos'
    sheet['F1'] = 'Intensidad'
    sheet['G1'] = 'Total Semana'
    sheet['H1'] = 'N° Profesores'
    sheet['I1'] = 'Total a Pagar'

    # Agregar datos a la hoja de cálculo
    row = 2
    for dato in datos:
        sheet.cell(row=row, column=1).value = dato['semestre']
        sheet.cell(row=row, column=2).value = dato['jornada']
        sheet.cell(row=row, column=3).value = dato['codigo']
        sheet.cell(row=row, column=4).value = dato['asignatura']
        sheet.cell(row=row, column=5).value = dato['creditos']
        sheet.cell(row=row, column=6).value = dato['intensidad']
        sheet.cell(row=row, column=7).value = dato['total_semana']
        sheet.cell(row=row, column=8).value = dato['num_profesores']
        sheet.cell(row=row, column=9).value = dato['total_a_pagar']
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
        semestre = proyeccion.semestre
        jornada = proyeccion.id_programas.jornada
        codigo = proyeccion.id_asignatura.codigo
        asignatura = proyeccion.id_asignatura.nombre
        creditos = proyeccion.id_asignatura.creditos
        intensidad = proyeccion.id_asignatura.intensidad
        total_semana = proyeccion.total_semana
        num_profesores = proyeccion.num_profesores

        datos.append({
            'semestre':semestre,
            'jornada': jornada,
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






def proyeccion_list(request):
    proyecciones = Proyeccion.objects.all()
    return render(request, 'editarProyeccion.html', {'proyecciones': proyecciones})


def editar_proyeccion(request, id):
    proyeccion = get_object_or_404(Proyeccion, id=id)
    if request.method == 'POST':
        form = ProyeccionForm(request.POST, instance=proyeccion)
        if form.is_valid():
            form.save()
            return redirect('/inicio/editar')
    else:
        form = ProyeccionForm(instance=proyeccion)

    return render(request, 'editarProyeccion.html', {'form': form})


from django.contrib.auth.decorators import login_required, user_passes_test


def disponibilidad(request):
    ordenar_por = request.GET.get('ordenar_por', 'fecha') # por defecto, ordenar por fecha
    disponibilidad = Disponibilidad.objects.order_by(ordenar_por)
    context = {
        'disponibilidad': disponibilidad,
        'ordenar_por': ordenar_por,
    }
    return render(request, 'verDispo.html', context)

@user_passes_test(lambda user: user.groups.filter(name='Profesores').exists())
def vista_para_profesor(request):
    if request.method == 'POST':
        form = DisponibilidadForm(request.POST)
        if form.is_valid():
            fecha = form.cleaned_data['fecha']
            hora_inicio = form.cleaned_data['hora_inicio']
            hora_fin = form.cleaned_data['hora_fin']

            # Validar que no se crucen los horarios
            disponibilidades = Disponibilidad.objects.filter(
                profesor=request.user,
                fecha=fecha,
                hora_inicio__lte=hora_fin,
                hora_fin__gte=hora_inicio
            )
            if disponibilidades.exists():
                return render(request, 'disponibilidad.html', {'form': form, 'error': 'El horario ya está ocupado.'})

            disponibilidad = Disponibilidad(
                fecha=fecha,
                hora_inicio=hora_inicio,
                hora_fin=hora_fin,
                comentarios=form.cleaned_data['comentarios'],
                profesor=request.user,
            )
            disponibilidad.save()
            return redirect('/inicio/disponibilidad')
    else:
        form = DisponibilidadForm()
    context = {'form': form}
    return render(request, 'disponibilidad.html', context)
"""  
import datetime
def vista_para_profesor(request):
    if request.method == 'POST':
        form = DisponibilidadForm(request.POST)
        if form.is_valid():
            fecha = form.cleaned_data['fecha']
            hora_inicio = form.cleaned_data['hora_inicio']
            hora_fin = form.cleaned_data['hora_fin']

            # Validar que no se crucen los horarios
            disponibilidades = Disponibilidad.objects.filter(
                profesor=request.user,
                fecha=fecha,
                hora_inicio__lte=hora_fin,
                hora_fin__gte=hora_inicio
            )
            if disponibilidades.exists():
                return render(request, 'disponibilidad.html', {'form': form, 'error': 'El horario ya está ocupado.'})

            disponibilidad = Disponibilidad(
                fecha=fecha,
                hora_inicio=hora_inicio,
                hora_fin=hora_fin,
                comentarios=form.cleaned_data['comentarios'],
                profesor=request.user,
            )
            disponibilidad.save()
            return redirect('/inicio/disponibilidad')
        else:
            return render(request, 'disponibilidad.html', {'form': form})
    else:
        fecha_seleccionada = request.GET.get('dia', 'lunes').capitalize()
        form = DisponibilidadForm(initial={'fecha': fecha_seleccionada})
        context = {'form': form, 'fecha_seleccionada': fecha_seleccionada}
        return render(request, 'disponibilidad.html', context)
"""

"""
from django.shortcuts import render, redirect
from django.contrib import messages
from .models import Programacion, Proyeccion

def crear_programacion(request):
    if request.method == 'POST':
        form = ProgramacionForm(request.POST)
        if form.is_valid():
            programacion = form.save()
            return redirect('/inicio/programacion', pk=programacion.pk)
    else:
        form = ProgramacionForm()
    return render(request, 'programacion.html', {'form': form})


"""
def ver_programacion(request):
    programaciones = Programacion.objects.all()
    proyecciones = Proyeccion.objects.all()
    return render(request, 'verProgramacion.html', {'programaciones': programaciones, 'proyecciones': proyecciones})

from django.utils import timezone
from django.contrib import messages
from django.shortcuts import render, redirect
from .forms import ProgramacionForm
from .models import Programacion, Proyeccion
"""
def crear_programacion(request):
    if request.method == 'POST':
        form = ProgramacionForm(request.POST)
        if form.is_valid():
            programacion = form.save(commit=False)
            # Verificar si el usuario tiene el rol de secretaría académica
            if request.user.groups.filter(name='secretaría académica').exists():
                # Obtener las fechas de inicio y fin de restricción
                fecha_inicio = timezone.datetime.strptime(request.POST.get('fecha_inicio'), '%Y-%m-%d')
                fecha_fin = timezone.datetime.strptime(request.POST.get('fecha_fin'), '%Y-%m-%d')
                # Verificar si la fecha de programación está dentro del rango de restricción
                if fecha_inicio <= programacion.proyeccion.fecha <= fecha_fin:
                    programacion.save()
                    messages.success(request, 'La programación se ha creado correctamente.')
                    return redirect('/inicio/programacion', pk=programacion.pk)
                else:
                    messages.error(request, 'La fecha de programación no está dentro del rango permitido.')
            else:
                # Si el usuario no tiene el rol de secretaría académica, guardar la programación sin restricciones
                programacion.save()
                messages.success(request, 'La programación se ha creado correctamente.')
                return redirect('/inicio/programacion', pk=programacion.pk)
    else:
        form = ProgramacionForm()
    return render(request, 'programacion.html', {'form': form})
""" 
from django.shortcuts import get_object_or_404
from django.contrib import messages
from django.shortcuts import redirect
from django.utils import timezone
from datetime import datetime

from django.utils import timezone

from django.db.models import Q
def crear_programacion(request):
    if request.method == 'POST':
        form = ProgramacionForm(request.POST)
        if form.is_valid():
            programacion = form.save(commit=False)
            # Verificar si el usuario pertenece a uno de los grupos restringidos
            if request.user.groups.filter(name__in=request.session.get('grupos', [])).exists():
                # Obtener las fechas de inicio y fin de restricción
                fecha_inicio = timezone.datetime.strptime(request.POST.get('fecha_inicio'), '%Y-%m-%d')
                fecha_fin = timezone.datetime.strptime(request.POST.get('fecha_fin'), '%Y-%m-%d')
                # Verificar si la fecha de programación está dentro del rango de restricción
                if fecha_inicio <= programacion.id_proyeccion.fecha <= fecha_fin:
                    programacion.save()
                    messages.success(request, 'La programación se ha creado correctamente.')
                    return redirect('/inicio/programacion', pk=programacion.pk)
                else:
                    messages.error(request, 'La fecha de programación no está dentro del rango permitido.')
            else:
                # Si el usuario no tiene el rol de secretaría académica ni pertenece a uno de los grupos restringidos, mostrar un mensaje de error
                messages.error(request, 'No tienes permisos para crear programaciones en este rango de fechas.')
    else:
        form = ProgramacionForm()
    return render(request, 'programacion.html', {'form': form})

"""

import datetime
def restringir_fechas(request):
    if request.method == 'POST':
        fecha_inicio = datetime.datetime.strptime(request.POST.get('fecha_inicio'), '%Y-%m-%d').strftime('%Y-%m-%d')
        fecha_fin = datetime.datetime.strptime(request.POST.get('fecha_fin'), '%Y-%m-%d').strftime('%Y-%m-%d')
        grupos_seleccionados = request.POST.getlist('grupos')  # obtener los grupos seleccionados
        grupos = []
        for grupo_id in grupos_seleccionados:
            grupo = Group.objects.get(id=grupo_id)
            grupos.append(grupo.id)
        # guardar las fechas y grupos en la sesión del usuario
        request.session['fecha_inicio'] = fecha_inicio
        request.session['fecha_fin'] = fecha_fin
        request.session['grupos'] = grupos
        messages.success(request, 'Se ha restringido el ingreso de programaciones para el rango de fechas seleccionado.')
        return redirect('ver_programacion')
    grupos = Group.objects.all()
    return render(request, 'restringirFechas.html', {'grupos': grupos})
"""

import datetime

from django.contrib import messages
from django.contrib.auth.models import Group
from django.db.models import Q
from django.shortcuts import render, redirect

from .models import Programacion

"""
def restringir_fechas(request):
    fecha_actual = datetime.datetime.now().strftime('%Y-%m-%d')
    if request.method == 'POST':
        if 'cancelar_restriccion' in request.POST:
            del request.session['fecha_inicio']
            del request.session['fecha_fin']
            del request.session['grupos']
            messages.success(request, 'Se ha cancelado la restricción de fechas.')
            return redirect('ver_programacion')
        else:
            fecha_inicio = datetime.datetime.strptime(request.POST.get('fecha_inicio'), '%Y-%m-%d').strftime('%Y-%m-%d')
            fecha_fin = datetime.datetime.strptime(request.POST.get('fecha_fin'), '%Y-%m-%d').strftime('%Y-%m-%d')
            grupos_seleccionados = request.POST.getlist('grupos')  # obtener los grupos seleccionados
            grupos = []
            for grupo_id in grupos_seleccionados:
                grupo = Group.objects.get(id=grupo_id)
                grupos.append(grupo.id)
            # guardar las fechas y grupos en la sesión del usuario
            request.session['fecha_inicio'] = fecha_inicio
            request.session['fecha_fin'] = fecha_fin
            request.session['grupos'] = grupos
            messages.success(request, 'Se ha restringido el ingreso de programaciones para el rango de fechas seleccionado.')
            return redirect('ver_programacion')
    grupos = Group.objects.all()
    return render(request, 'restringirFechas.html', {'grupos': grupos,'fecha_actual': fecha_actual})
""" 


def restringir_fechas(request):
    

    fecha_actual = datetime.datetime.now().strftime('%Y-%m-%d')
    if request.method == 'POST':
        if 'cancelar_restriccion' in request.POST:
            del request.session['fecha_inicio']
            del request.session['fecha_fin']
            del request.session['grupo']  # cambia de grupos a grupo
            messages.success(request, 'Se ha cancelado la restricción de fechas.')
            return redirect('ver_programacion')
        else:
            fecha_inicio = datetime.datetime.strptime(request.POST.get('fecha_inicio'), '%Y-%m-%d').strftime('%Y-%m-%d')
            fecha_fin = datetime.datetime.strptime(request.POST.get('fecha_fin'), '%Y-%m-%d').strftime('%Y-%m-%d')
            grupo_id = request.POST.get('grupo')  # obtener el grupo seleccionado
            grupo = Group.objects.get(id=grupo_id)
            # guardar las fechas y el grupo en la sesión del usuario
            request.session['fecha_inicio'] = fecha_inicio
            request.session['fecha_fin'] = fecha_fin
            request.session['grupo'] = grupo.id  # cambia de grupos a grupo
            messages.success(request, f'Se ha restringido el ingreso de programaciones para el rango de fechas seleccionado en el grupo {grupo.name}.')
            return redirect('ver_programacion')
    grupos = Group.objects.all()

    return render(request, 'restringirFechas.html', {'grupos': grupos,'fecha_actual': fecha_actual})


def ver_restricciones_fechas(request):
    fecha_inicio = request.session.get('fecha_inicio')
    fecha_fin = request.session.get('fecha_fin')
    grupo_id = request.session.get('grupo')
    grupo = Group.objects.get(id=grupo_id) if grupo_id else None
    return render(request, 'verRestricciones.html', {'fecha_inicio': fecha_inicio, 'fecha_fin': fecha_fin, 'grupo': grupo})



def quitar_restricciones(request):
    # Eliminar las variables de sesión relacionadas con las restricciones
    del request.session['fecha_inicio']
    del request.session['fecha_fin']
    del request.session['grupo']
    
    # Redireccionar a la página de programación sin restricciones
    messages.success(request, 'Todas las restricciones han sido eliminadas.')
    return redirect('ver_programacion')