from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.models import User
from django.contrib.auth.models import Group
from .models import Disponibilidad, Programas, Asignatura, Proyeccion,Programacion

class LoginForm(AuthenticationForm):
    username = forms.CharField(
        max_length=254,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Nombre de usuario'
        })
    )
    password = forms.CharField(label="Contraseña", strip=False,widget=forms.PasswordInput(attrs={'class': 'form-control','placeholder':'Contraseña'}))





class registro_form(forms.ModelForm):
    
    email = forms.EmailField(required=True, label='Email', widget=forms.EmailInput(attrs={'class': 'form-control','placeholder':'Ejemplo:messi@gmail.com'}))
    username = forms.CharField(required=True, label='Nombre de usuario', widget=forms.TextInput(attrs={'class': 'form-control','placeholder':'Ejemplo:messi'}))
    first_name = forms.CharField(required=True, label='Nombre', widget=forms.TextInput(attrs={'class': 'form-control','placeholder':'Ejemplo:Leo'}))
    last_name = forms.CharField(required=True, label='Apellido', widget=forms.TextInput(attrs={'class': 'form-control','placeholder':'Ejemplo:Messi'}))
    password1 = forms.CharField(label="Contraseña", strip=False,widget=forms.PasswordInput(attrs={'class': 'form-control','placeholder':'Contraseña'}))
    password2 = forms.CharField(label="Confirmar contraseña", strip=False,widget=forms.PasswordInput(attrs={'class': 'form-control','placeholder':'Contraseña'}))
    group = forms.ModelChoiceField(queryset=Group.objects.all(), required=True, label='Grupo', widget=forms.Select(attrs={'class': 'form-control'}))
    class Meta:
        model = User
        fields = ('email', 'username', 'first_name', 'last_name', 'password1', 'password2', 'group')

    def clean_password2(self):
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError('Las contraseñas no coinciden.')
        return password2

    def save(self, commit=True):
        user = super(registro_form, self).save(commit=False)
        user.email = self.cleaned_data['email']
        user.username = self.cleaned_data['username']
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        user.set_password(self.cleaned_data['password1'])
        if commit:
            user.save()
            if self.cleaned_data['group']:
                group = self.cleaned_data['group']
                user.groups.add(group)
        
        return user





class EditUserForm(forms.ModelForm):
    email = forms.EmailField(required=True, label='Email', widget=forms.EmailInput(attrs={'class': 'form-control','placeholder':'Ejemplo:messi@gmail.com'}))
    username = forms.CharField(required=True, label='Nombre de usuario', widget=forms.TextInput(attrs={'class': 'form-control','placeholder':'Ejemplo:messi'}))
    first_name = forms.CharField(required=True, label='Nombre', widget=forms.TextInput(attrs={'class': 'form-control','placeholder':'Ejemplo:Leo'}))
    last_name = forms.CharField(required=True, label='Apellido', widget=forms.TextInput(attrs={'class': 'form-control','placeholder':'Ejemplo:Messi'}))
    group = forms.ModelChoiceField(queryset=Group.objects.all(), required=True, label='Grupo', widget=forms.Select(attrs={'class': 'form-control'}))

    class Meta:
        model = User
        fields = ['email', 'username', 'first_name', 'last_name', 'group']
        

class ProyeccionForm(forms.ModelForm):
    class Meta:
        model = Proyeccion
        fields = ('id_programas', 'id_asignatura','semestre')
        widgets = {
            
            'id_programas': forms.Select(attrs={'class': 'form-control'}),
            'id_asignatura': forms.Select(attrs={'class': 'form-control'}),
            'semestre': forms.NumberInput(attrs={'class': 'form-control'}),
        }
        
        
class ProyeccionForm1(forms.ModelForm):
    class Meta:
        model = Proyeccion
        fields = ('id_programas', 'id_asignatura')
        
        
        
from django import forms
"""
class DisponibilidadForm(forms.Form):
    fecha = forms.DateField(widget=forms.TextInput(attrs={'type': 'date', 'class': 'form-control'}))
    hora_inicio = forms.TimeField(widget=forms.TextInput(attrs={'type': 'time', 'class': 'form-control'}))
    hora_fin = forms.TimeField(widget=forms.TextInput(attrs={'type': 'time', 'class': 'form-control'}))
    comentarios = forms.CharField(widget=forms.Textarea(attrs={'class': 'form-control'}))
"""
class DisponibilidadForm(forms.Form):
    DAY_CHOICES = [
        ('LUNES', 'Lunes'),
        ('MARTES', 'Martes'),
        ('MIERCOLES', 'Miércoles'),
        ('JUEVES', 'Jueves'),
        ('VIERNES', 'Viernes'),
        ('SABADO', 'Sábado'),
        ('DOMINGO', 'Domingo'),
    ]
    
    fecha = forms.ChoiceField(choices= DAY_CHOICES, widget=forms.Select(attrs={'class': 'form-control'}))
    hora_inicio = forms.TimeField(widget=forms.TextInput(attrs={'type': 'time', 'class': 'form-control'}))
    hora_fin = forms.TimeField(widget=forms.TextInput(attrs={'type': 'time', 'class': 'form-control'}))
    comentarios = forms.CharField(initial='Disponible', widget=forms.Textarea(attrs={'class': 'form-control'}))

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['comentarios'].required = False




class ProgramacionForm(forms.ModelForm):
    DAY_CHOICES = [
        ('LUNES', 'Lunes'),
        ('MARTES', 'Martes'),
        ('MIERCOLES', 'Miércoles'),
        ('JUEVES', 'Jueves'),
        ('VIERNES', 'Viernes'),
        ('SABADO', 'Sábado'),
        ('DOMINGO', 'Domingo'),
    ]
    
    proyeccion = forms.ModelChoiceField(queryset=Proyeccion.objects.all(), widget=forms.Select(attrs={'class': 'form-control'}))
    dia = forms.ChoiceField(choices=DAY_CHOICES, widget=forms.Select(attrs={'class': 'form-control'}))
    hora = forms.TimeField(widget=forms.TextInput(attrs={'type': 'time', 'class': 'form-control'}))

    def clean_dia(self):
        return self.cleaned_data['dia'].upper()

    def save(self, commit=True):
        programacion = super(ProgramacionForm, self).save(commit=False)
        programacion.id_proyeccion_id = self.cleaned_data['proyeccion'].id
        if commit:
            programacion.save()
        return programacion

    class Meta:
        model = Programacion
        fields = ['proyeccion', 'dia', 'hora']
        
        
        

from django import forms

class RestringirFechasForm(forms.Form):
    grupos = forms.ModelMultipleChoiceField(
        queryset=Group.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        label="Grupos a restringir"
    )
    fecha_inicio = forms.DateField(label="Fecha de inicio")
    fecha_fin = forms.DateField(label="Fecha de fin")