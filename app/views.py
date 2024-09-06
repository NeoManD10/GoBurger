from django.shortcuts import render, redirect
from .forms import LoginForm
from .models import Ingrediente
from .forms import RegisterForm

def login_view(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            # Aquí puedes guardar algo en la sesión para indicar que el usuario ha iniciado sesión
            request.session['usuario_id'] = form.cleaned_data['email']
            return redirect('home')  # Redirigir a la página de inicio o a donde quieras
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
            form.save()  # Guardamos el nuevo usuario
            return redirect('login')  # Redirigimos al login después de registrarse
    else:
        form = RegisterForm()

    return render(request, 'register.html', {'form': form})
