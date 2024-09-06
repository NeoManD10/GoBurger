from django import forms
from .models import Usuario

class LoginForm(forms.Form):
    email = forms.EmailField(max_length=150, required=True)
    contrasena = forms.CharField(widget=forms.PasswordInput, required=True)  # Cambia aquí

    def clean(self):
        email = self.cleaned_data.get('email')
        contrasena = self.cleaned_data.get('contrasena')  # Cambia aquí también

        try:
            usuario = Usuario.objects.get(email=email)
        except Usuario.DoesNotExist:
            raise forms.ValidationError("Usuario no encontrado.")

        if usuario.contrasena != contrasena:  # Cambia aquí también
            raise forms.ValidationError("Contraseña incorrecta.")

        return self.cleaned_data

class RegisterForm(forms.ModelForm):
    contrasena = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = Usuario
        fields = ['nombre', 'email', 'contrasena']  # Campos que quieres que el usuario complete

