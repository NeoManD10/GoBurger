from django import forms
from app.models import Usuario
from django.core.mail import send_mail
import random


class GenerarResetCode(forms.Form):
    email = forms.EmailField(max_length=150, required=True)

    def clean_email(self):
        email = self.cleaned_data['email']
        try:
            # Store the user in the instance variable for later access
            self.usuario = Usuario.objects.get(email=email)
        except Usuario.DoesNotExist:
            raise forms.ValidationError("El usuario no existe.")
        return email

    def save(self):
        # Generate a unique reset code
        reset_code = str(random.randint(1000, 9999))  # Keep as string
        # Save the reset code to the user
        self.usuario.reset_code = reset_code
        self.usuario.save()
        # Send the email with the reset code
        self.send_email(reset_code)

    def send_email(self, reset_code):
        subject = "GoyoBurger: Cambiar contraseña"
        message = f"Tu código para el cambio de contraseña es: {reset_code}"
        send_mail(subject, message, 'vtapiad@utem.cl', [self.usuario.email])

class VerificarResetCode(forms.Form):
    code = forms.CharField(max_length=4, required=True)


class ActualizarContrasena(forms.Form):
    contrasena = forms.CharField(widget=forms.PasswordInput, required=True)
