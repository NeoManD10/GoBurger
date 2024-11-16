from django.contrib.auth.decorators import login_required
from django.contrib import messages #Permite mostrar mensajes al usuario, como alertas de éxito o error, que se pueden ver en la plantilla.
from django.http import HttpResponse
from django.conf import settings
from django.shortcuts import render, redirect #Render rinde una plantilla HTML y devuelve una respuesta con el contenido HTML, mientras que redirect redirige al usuario a otra URL.
from app.forms import LoginForm, RegisterForm #Formularios personalizados para el inicio de sesión y registro de usuario.
from app.models import Usuario, Ingrediente,HistorialPedido, PedidoIngrediente, HistorialPedido #Modelos de la BDD
from reportlab.lib.pagesizes import letter # type: ignore
from reportlab.pdfgen import canvas # type: ignore
from datetime import datetime
import random

def login_view(request):
    if request.method == 'POST':  # Verifica si el formulario fue enviado con el método POST
        form = LoginForm(request.POST)  # Crea una instancia de LoginForm con los datos enviados en el formulario
        if form.is_valid():  # Comprueba que los datos del formulario sean válidos
            email = form.cleaned_data['email']  # Extrae el email del formulario validado
            contrasena = form.cleaned_data['contrasena']  # Extrae la contraseña del formulario validado
            try:
                usuario = Usuario.objects.get(email=email, contrasena=contrasena)  # Busca un usuario con el email y contraseña proporcionados
                request.session['usuario_id'] = usuario.id  # Guarda el ID del usuario en la sesión para mantener la autenticación
                request.session['usuario_nombre'] = usuario.nombre  # Guarda el nombre del usuario en la sesión
                return redirect('home')  # Redirige a la página de inicio si el inicio de sesión es exitoso
            except Usuario.DoesNotExist:  # Captura el error si no se encuentra el usuario
                form.add_error(None, "Email o contraseña incorrectos")  # Agrega un error al formulario si las credenciales son incorrectas
    else:
        form = LoginForm()  # Si no es POST, crea un formulario vacío para el inicio de sesión
    return render(request, 'login.html', {'form': form})  # Rinde la plantilla de inicio de sesión con el formulario



def home(request):
    if 'usuario_id' in request.session:  # Verifica si el usuario ha iniciado sesión (ID del usuario en la sesión)
        usuario_id = request.session['usuario_id']  # Obtiene el ID del usuario de la sesión
        historial_completo = HistorialPedido.objects.filter(usuario_id=usuario_id).select_related('usuario')  # Obtiene el historial de pedidos para el usuario
        pedidos_con_ingredientes = []  # Lista para almacenar pedidos con sus ingredientes

        for pedido in historial_completo:  # Itera sobre cada pedido en el historial
            ingredientes = PedidoIngrediente.objects.filter(pedido=pedido)  # Obtiene los ingredientes para cada pedido
            pedidos_con_ingredientes.append({'pedido': pedido, 'ingredientes': ingredientes})  # Agrega el pedido y sus ingredientes a la lista

        return render(request, 'home.html', {
            'historial_completo': pedidos_con_ingredientes  # Pasa el historial completo a la plantilla
        })
    else:
        return render(request, 'home.html', {
            'historial_completo': None  # Si no hay usuario autenticado, no muestra el historial
        })


def register_view(request):
    if request.method == 'POST':  # Verifica si el formulario fue enviado con el método POST
        form = RegisterForm(request.POST)  # Crea una instancia de RegisterForm con los datos del formulario
        if form.is_valid():  # Verifica que los datos del formulario sean válidos
            usuario = form.save()  # Guarda el nuevo usuario en la base de datos
            request.session['usuario_id'] = usuario.id  # Guarda el ID del usuario en la sesión
            request.session['usuario_nombre'] = usuario.nombre.split(' ')[0]  # Guarda el primer nombre del usuario en la sesión
            return redirect('home')  # Redirige a la página de inicio si el registro fue exitoso
    else:
        form = RegisterForm()  # Si no es POST, crea un formulario vacío de registro

    return render(request, 'register.html', {'form': form})  # Rinde la plantilla de registro con el formulario

@login_required
def ingredientes_view(request):
      

    ingredientes = Ingrediente.objects.all()  # Obtiene todos los ingredientes disponibles

    if request.method == 'POST':  # Verifica si el formulario fue enviado con el método POST
        ingredientes_ids = request.POST.getlist('ingredientes')  # Obtiene los IDs de los ingredientes seleccionados

        if not ingredientes_ids:  # Verifica si no se seleccionaron ingredientes
            return redirect('ingredientes')  # Redirige a la misma página de selección de ingredientes

        usuario_id = request.session.get('usuario_id')  # Obtiene el ID del usuario desde la sesión
        if not usuario_id:  # Si el usuario no ha iniciado sesión
            messages.error(request, "Debes iniciar sesión para hacer un pedido.")  # Muestra un mensaje de error
            return redirect('login')  # Redirige a la página de inicio de sesión

        historial_pedido = HistorialPedido.objects.create(usuario_id=usuario_id)  # Crea un nuevo registro en el historial de pedidos

        for ingrediente_id in ingredientes_ids:  # Itera sobre los IDs de ingredientes seleccionados
            ingrediente = Ingrediente.objects.get(id=ingrediente_id)  # Obtiene cada ingrediente por su ID
            PedidoIngrediente.objects.create(pedido=historial_pedido, ingrediente=ingrediente)  # Crea un registro en PedidoIngrediente para asociar el ingrediente al pedido

        messages.success(request, "Pedido realizado con éxito.")  # Muestra un mensaje de éxito
        return redirect('carrito')  # Redirige a la vista del carrito

    return render(request, 'ingredientes.html', {'ingredientes': ingredientes})  # Rinde la plantilla con la lista de ingredientes


def logout_view(request):
    if 'usuario_nombre' in request.session:  # Verifica si 'usuario_nombre' está en la sesión
        del request.session['usuario_nombre']  # Elimina 'usuario_nombre' de la sesión
    return redirect('home')  # Redirige a la página principal

@login_required
def historial_view(request):
    usuario_id = request.session.get('usuario_id')  # Obtiene el ID del usuario desde la sesión
    if not usuario_id:  # Si el usuario no ha iniciado sesión
        messages.error(request, "Debes iniciar sesión para ver tu historial.")  # Muestra un mensaje de error
        return redirect('login')  # Redirige a la página de inicio de sesión

    historial_pedidos = HistorialPedido.objects.filter(usuario_id=usuario_id)  # Obtiene el historial de pedidos del usuario
    return render(request, 'historial.html', {'historial_pedidos': historial_pedidos})  # Rinde la plantilla del historial


def carrito_view(request):
    usuario_id = request.session.get('usuario_id')  # Obtiene el ID del usuario desde la sesión
    historial_pedido = HistorialPedido.objects.filter(usuario_id=usuario_id).last()  # Obtiene el último pedido del historial del usuario

    ingredientes = PedidoIngrediente.objects.filter(pedido=historial_pedido)  # Obtiene los ingredientes del último pedido
    total_precio = sum([ingrediente.ingrediente.precio for ingrediente in ingredientes])  # Calcula el precio total del pedido

    return render(request, 'carrito.html', {
        'ingredientes': ingredientes,  # Pasa la lista de ingredientes a la plantilla
        'total_precio': total_precio  # Pasa el total del pedido a la plantilla
    })

def generar_boleta_pdf(request):
    usuario_id = request.session.get('usuario_id')
    if not usuario_id:
        messages.error(request, "Debes iniciar sesión para generar la boleta.")
        return redirect('login')

    # Obtén el último pedido del usuario
    historial_pedido = HistorialPedido.objects.filter(usuario_id=usuario_id).last()
    ingredientes = PedidoIngrediente.objects.filter(pedido=historial_pedido)
    total_precio = sum([ingrediente.ingrediente.precio for ingrediente in ingredientes])

    # Configura la respuesta HTTP para el PDF
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="boleta.pdf"'

    # Crea el PDF
    p = canvas.Canvas(response, pagesize=letter)
    p.setFont("Helvetica", 12)

    # Agrega título y fecha/hora
    p.drawString(100, 750, "Boleta de Compra - GoyoBurger")
    p.drawString(100, 730, f"Fecha y Hora: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

    # Detalles del pedido
    y_position = 700
    for ingrediente in ingredientes:
        p.drawString(100, y_position, f"{ingrediente.ingrediente.nombre} - ${ingrediente.ingrediente.precio}")
        y_position -= 20

    # Total
    p.drawString(100, y_position - 20, f"Total del Pedido: ${total_precio}")

    # Guarda el PDF
    p.showPage()
    p.save()

    return response

def about_us_view(request):
    return render(request, 'about_us.html')

