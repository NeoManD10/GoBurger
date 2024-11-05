from django import forms #crear formularios personalizados y de modelo.
from .models import Usuario #Importa el modelo Usuario desde el archivo models.py, para que podamos utilizarlo en los formularios.
import random 

class LoginForm(forms.Form):  # Define un formulario de Django llamado LoginForm, que hereda de forms.Form, lo cual indica que es un formulario estándar.
    email = forms.EmailField(max_length=150, required=True) # Define un campo de tipo EmailField que espera una dirección de correo válida.
    contrasena = forms.CharField(widget=forms.PasswordInput, required=True)  # Define un campo de tipo CharField para la contraseña.

    def clean(self): # Define el método clean, que se utiliza para realizar validaciones adicionales en el formulario después de que se han ingresado los datos.
        email = self.cleaned_data.get('email') # Extrae el valor de email de cleaned_data, que es un diccionario que contiene los datos validados del formulario.
        contrasena = self.cleaned_data.get('contrasena')  # Extrae el valor de contrasena.

        try:
            usuario = Usuario.objects.get(email=email) # Busca un usuario en la base de datos cuyo email coincida con el email ingresado en el formulario
            if usuario.contrasena != contrasena:
                raise forms.ValidationError("Contraseña incorrecta.") 
        except Usuario.DoesNotExist:
            raise forms.ValidationError("El usuario no existe.")
        
        return self.cleaned_data #Retorna los datos validados si todas las validaciones se pasaron correctamente

class RegisterForm(forms.ModelForm): #Define el formulario RegisterForm, que hereda de forms.ModelForm
    contrasena = forms.CharField(widget=forms.PasswordInput) #Agrega un campo de contraseña al formulario.

    class Meta: #Define opciones adicionales para el formulario.
        model = Usuario
        fields = ['nombre', 'email', 'contrasena']  # Campos que quieres que el usuario complete
