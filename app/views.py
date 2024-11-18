from django.contrib.auth.decorators import login_required
from django.contrib import messages #Permite mostrar mensajes al usuario, como alertas de éxito o error, que se pueden ver en la plantilla.
from django.http import HttpResponse
from django.conf import settings
from django.shortcuts import render, redirect, get_object_or_404 #Render rinde una plantilla HTML y devuelve una respuesta con el contenido HTML, mientras que redirect redirige al usuario a otra URL.
from app.forms import LoginForm, RegisterForm #Formularios personalizados para el inicio de sesión y registro de usuario.
from app.models import Usuario, Ingrediente, HistorialPedido, PedidoIngrediente, HistorialPedido, Carrito #Modelos de la BDD
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
        historial_completo = HistorialPedido.objects.filter(usuario_id=usuario_id, activo=False).select_related('usuario')  # Obtiene el historial de pedidos para el usuario
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


def logout_view(request):
    if 'usuario_nombre' in request.session:  # Verifica si 'usuario_nombre' está en la sesión
        del request.session['usuario_nombre']  # Elimina 'usuario_nombre' de la sesión
    return redirect('home')  # Redirige a la página principal


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
        pedido_ingredientes = PedidoIngrediente.objects.filter(pedido=historial_pedido)
        carrito = get_or_create_carrito(request)

        for pedido_ingrediente in pedido_ingredientes:
            anadir_a_carrito_view(request, pedido_ingrediente)
        carrito.save()
        return redirect('carrito')  # Redirige a la vista del carrito

    return render(request, 'ingredientes.html', {'ingredientes': ingredientes})  # Rinde la plantilla con la lista de ingredientes


def logout_view(request):
    if 'usuario_nombre' in request.session:  # Verifica si 'usuario_nombre' está en la sesión
        del request.session['usuario_nombre']  # Elimina 'usuario_nombre' de la sesión
    return redirect('home')  # Redirige a la página principal


def historial_view(request):
    usuario_id = request.session.get('usuario_id')  # Obtiene el ID del usuario desde la sesión
    if not usuario_id:  # Si el usuario no ha iniciado sesión
        messages.error(request, "Debes iniciar sesión para ver tu historial.")  # Muestra un mensaje de error
        return redirect('login')  # Redirige a la página de inicio de sesión

    # Ordenamos por fecha en orden descendente
    historial_pedidos = HistorialPedido.objects.filter(
        activo=False, usuario_id=usuario_id
    ).order_by('fecha_pedido')  # Ordenamos por fecha_pedido en orden descendente

    return render(request, 'historial.html', {'historial_pedidos': historial_pedidos})  # Enviamos la lista ordenada



def get_or_create_carrito(request):
    usuario_id = request.session.get('usuario_id')  # Obtiene el ID del usuario desde la sesión
    if not usuario_id:  # Si el usuario no ha iniciado sesión
        return redirect('login')  # Redirige a la página de inicio de sesión
    carrito, created = Carrito.objects.get_or_create(usuario_id=usuario_id)  # Filtro por usuario_id
    return carrito  # Retorna el carrito


def vista_carrito_view(request):
    carrito = get_or_create_carrito(request)
    pedidos = carrito.pedidos_guardados.all()
    costo_total = 0
    for pedido_ingrediente in carrito.pedidos_guardados.all():
        costo_total += pedido_ingrediente.ingrediente.precio
    return render(request, 'carrito.html', {'carrito': carrito, 'pedidos': pedidos, 'costo_total': costo_total})


def anadir_a_carrito_view(request, pedido):
    carrito = get_or_create_carrito(request)  # Obtiene el carrito del usuario
    if isinstance(carrito, HttpResponse):  # Verifica si hubo una redirección
        return carrito  # Redirige al login si no existe el carrito
    carrito.pedidos_guardados.add(pedido)
    carrito.save()
    return redirect('carrito')

def borrar_del_carrito_view(request, pedido_id):
    if request.method == "POST":
        carrito = get_or_create_carrito(request)
        pedidos = carrito.pedidos_guardados.filter(pedido__id=pedido_id)
        pedidos.delete()
    return redirect('carrito')


def generar_boleta_pdf(request):
    usuario_id = request.session.get('usuario_id')
    if not usuario_id:
        messages.error(request, "Debes iniciar sesión para generar la boleta.")
        return redirect('login')
    carrito = get_or_create_carrito(request)
    pedidos = carrito.pedidos_guardados.all()
    costo_total = 0

    # Configura la respuesta HTTP para el PDF
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="boleta.pdf"'

    # Crea el PDF
    p = canvas.Canvas(response, pagesize=letter)
    p.setFont("Helvetica", 12)

    # Agrega título y fecha/hora
    p.setFont("Helvetica-Bold", 14)
    p.drawString(100, 750, "Boleta de Compra - GoyoBurger")
    p.drawString(100, 730, f"Fecha y Hora: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

    # Detalles del pedido
    y_position = 700
    anterior_id = -1
    n_pedido = 1
    contador = 0
    if not carrito.pedidos_guardados.exists():
        return redirect('carrito')
    for pedido in pedidos:
        if y_position < 100:
            p.showPage()  # Crea nueva página
            p.setFont("Helvetica-Bold", 14)
            y_position = 750  # Devuelve la impresión al inicio de la página
            p.drawString(100, y_position, "Boleta de Compra - GoyoBurger")
            p.drawString(100, y_position - 20, f"Fecha y Hora: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
            y_position -= 60  # Espacio para separar

        if(anterior_id != pedido.pedido.id):
            contador += 1
            p.setFont("Helvetica-Bold", 12)
            p.drawString(100, y_position, f"Pedido N°{n_pedido}")
            y_position -= 20
            n_pedido += 1
        p.setFont("Helvetica", 10)
        p.drawString(100, y_position, f"{pedido.ingrediente.nombre} - ${pedido.ingrediente.precio}")
        y_position -= 20
        costo_total += pedido.ingrediente.precio
        anterior_id = pedido.pedido.id

    # Total
    p.setFont("Helvetica-Bold", 16)
    p.drawString(100, y_position - 20, f"Total del Pedido: ${costo_total}")
    anterior_id = -1
    historial_pedido = HistorialPedido.objects.create(usuario_id=usuario_id, activo=False)
    for pedido_ingrediente in carrito.pedidos_guardados.all():
        pedido_ingrediente.pedido = historial_pedido
        pedido_ingrediente.save()


    # Guarda el PDF
    p.showPage()
    p.save()
    carrito.pedidos_guardados.clear()
    return response

def about_us_view(request):
    return render(request, 'about_us.html')

