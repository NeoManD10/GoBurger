from django.shortcuts import render, redirect
from .forms import LoginForm, RegisterForm
from .models import Usuario, Ingrediente

def login_view(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            contrasena = form.cleaned_data['contrasena']
            try:
                usuario = Usuario.objects.get(email=email, contrasena=contrasena)
                request.session['usuario_id'] = usuario.id  # Guardar en la sesión
                request.session['usuario_nombre'] = usuario.nombre.split(' ')[0]  # Guardar el primer nombre en la sesión
                return redirect('home')  # Redirigir a la página principal
            except Usuario.DoesNotExist:
                form.add_error(None, "Email o contraseña incorrectos")
    else:
        form = LoginForm()
    return render(request, 'login.html', {'form': form})

def home(request):
    return render(request, 'home.html')

def ingredientes_view(request):
    ingredientes = Ingrediente.objects.all()  # Obtener todos los ingredientes
    return render(request, 'ingredientes.html', {'ingredientes': ingredientes})

def register_view(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            usuario = form.save()  # Guardamos el nuevo usuario
            request.session['usuario_id'] = usuario.id  # Guardar en la sesión
            request.session['usuario_nombre'] = usuario.nombre.split(' ')[0]  # Guardar el primer nombre en la sesión
            return redirect('home')  # Redirigir a la página de inicio
    else:
        form = RegisterForm()

    return render(request, 'register.html', {'form': form})

def ingredientes_view(request):
    ingredientes = Ingrediente.objects.all()  # Obtén todos los ingredientes de la base de datos
    return render(request, 'ingredientes.html', {'ingredientes': ingredientes})

