from django import forms
from django.core.exceptions import ValidationError
from django.contrib.auth  import get_user_model

User = get_user_model()

class LoginForm(forms.Form):
    username = forms.CharField(
    label="Nombre de Usuario",
    max_length=150,
    widget=forms.TextInput(attrs={'placeholder': 'Tu nombre de usuario'})
    )

    password = forms.CharField(
    label="Contraseña",
    widget=forms.PasswordInput(attrs={'placeholder': 'Tu contraseña'})
    )

class RegisterForm(forms.Form):
    username = forms.CharField(
        label="Nombre de Usuario",
        max_length=150,
        widget=forms.TextInput(attrs={'placeholder': 'Define tu nombre de usuario'})
    )
    
    email = forms.EmailField(
        label="Correo Electrónico",
        widget=forms.EmailInput(attrs={'placeholder': 'Tu correo electrónico'})
    )

    password = forms.CharField(
        label="Contraseña",
        widget=forms.PasswordInput(attrs={'placeholder': 'Define tu contraseña'})
    )

    confirm_password = forms.CharField(
        label="Confirmar Contraseña",
        widget=forms.PasswordInput(attrs={'placeholder': 'Confirma tu contraseña'})
    )

    def clean_username(self):
        username = self.cleaned_data['username']
        if User.objects.filter(username=username).exists():
            raise ValidationError("El nombre de usuario ya está en uso.")
        return username

    def clean_email(self):
        email = self.cleaned_data['email']
        if User.objects.filter(email=email).exists():
            raise ValidationError("El correo electrónico ya está en uso.")
        return email
    
    def clean(self):
        cleaned_data= super().clean()
        password = cleaned_data.get('password')
        password_confirm = cleaned_data.get('confirm_password')
        
        if password and password_confirm and password != password_confirm:
            raise ValidationError("Las contraseñas no coinciden.")
        return cleaned_data