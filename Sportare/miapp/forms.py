from django import forms
from django.core import validators
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Mensajes, Usuario


class RegisterForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'password1', 'password2']

class MensajesForm(forms.ModelForm):
    class Meta:
        model = Mensajes
        fields = ['nombre', 'email', 'texto']  # Campos que aparecerán en el formulario
        
class UsuarioForm(forms.ModelForm):
    class Meta:
        model = Usuario
        fields = ['nombre', 'apellidos', 'dni', 'telefono', 'email', 'ciudad', 'direccion']