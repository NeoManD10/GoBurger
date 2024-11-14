from django.contrib import messages
from django.http import HttpResponse
from django.conf import settings
from django.core.mail import send_mail
from django.shortcuts import render, redirect
from app_2.forms import GenerarResetCode, VerificarResetCode, ActualizarContrasena
from app.models import Usuario
import random

def generar_reset_code_view(request): # Genera el codigo que el usuario usa para recuperar la contraseña
    if request.method == "POST":
        form = GenerarResetCode(request.POST)
        if form.is_valid():
            user = form.usuario
            form.save()
            request.session["email_usuario"] = user.email
            return redirect('verificar-reset-code')
    else:
        form = GenerarResetCode()
    return render(request, 'generar-reset-code.html', {'form': form})

def verificar_reset_code_view(request): # Verificacion del codigo para actualizar la contraseña
    email = request.session.get("email_usuario")
    if not email:
        return HttpResponse("Acceso denegado.", status=404)

    if request.method == "POST":
        form = VerificarResetCode(request.POST)
        if form.is_valid():
            code = form.cleaned_data['code']
            try:
                user = Usuario.objects.get(email=email, reset_code=code)
                return redirect("actualizar-contrasena")    # Si funciona se tira a actualizar la contraseña
            except Usuario.DoesNotExist:
                return HttpResponse("Código inválido.", status=404)
    else:
        form = VerificarResetCode()

    return render(request, "verificar-reset-code.html", {"form": form})

def actualizar_contrasena_view(request):
    email = request.session.get("email_usuario")
    if not email:
        return HttpResponse("Acceso denegado.", status=404) # Si se intenta acceder sin codigo

    if request.method == "POST":
        form = ActualizarContrasena(request.POST)
        if form.is_valid():
            contrasena = form.cleaned_data['contrasena']
            try:
                usuario = Usuario.objects.get(email=email)
                usuario.contrasena = contrasena
                usuario.save()  # Guarda la contraseña
                del request.session['email_usuario'] # Cierra la sesion y retorna al login
                return redirect("login")
            except Usuario.DoesNotExist:
                return HttpResponse("Usuario no encontrado.", status=404)
    else:
        form = ActualizarContrasena()

    return render(request, "actualizar-contrasena.html", {"form": form})
