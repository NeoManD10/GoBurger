from django.contrib import messages #Permite mostrar mensajes al usuario, como alertas de éxito o error, que se pueden ver en la plantilla.
from django.http import HttpResponse
from django.conf import settings
from django.core.mail import send_mail
from django.shortcuts import render, redirect #Render rinde una plantilla HTML y devuelve una respuesta con el contenido HTML, mientras que redirect redirige al usuario a otra URL.
from app.forms import LoginForm, RegisterForm #Formularios personalizados para el inicio de sesión y registro de usuario.
from app_2.forms import GenerarResetCode, VerificarResetCode, ActualizarContrasena
from app.models import Usuario, Ingrediente,HistorialPedido, PedidoIngrediente, HistorialPedido #Modelos de la BDD
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


def ingredientes_view(request):
    ingredientes = Ingrediente.objects.all()  # Obtiene todos los ingredientes disponibles

    if request.method == 'POST':  # Verifica si el formulario fue enviado con el método POST
        ingredientes_ids = request.POST.getlist('ingredientes')  # Obtiene los IDs de los ingredientes seleccionados

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


def seleccionar_ingredientes_view(request):
    ingredientes = Ingrediente.objects.filter(disponible=True)  # Obtiene todos los ingredientes disponibles (filtro `disponible=True`)

    if request.method == 'POST':  # Verifica si el formulario fue enviado con el método POST
        usuario_id = request.session.get('usuario_id')  # Obtiene el ID del usuario desde la sesión
        if not usuario_id:  # Si el usuario no ha iniciado sesión
            return redirect('login')  # Redirige a la página de inicio de sesión

        pedido = HistorialPedido.objects.create(usuario_id=usuario_id)  # Crea un nuevo historial de pedido para el usuario
        ingredientes_seleccionados = request.POST.getlist('ingredientes')  # Obtiene los IDs de los ingredientes seleccionados
        precio_total = 0  # Variable para calcular el precio total del pedido

        for ingrediente_id in ingredientes_seleccionados:  # Itera sobre los IDs de ingredientes seleccionados
            ingrediente = Ingrediente.objects.get(id=ingrediente_id)  # Obtiene cada ingrediente por su ID
            PedidoIngrediente.objects.create(pedido=pedido, ingrediente=ingrediente)  # Crea un registro en PedidoIngrediente
            precio_total += ingrediente.precio  # Suma el precio del ingrediente al total

        request.session['precio_total'] = precio_total  # Guarda el precio total en la sesión
        return redirect('resumen_pedido')  # Redirige a la vista de resumen del pedido

    return render(request, 'ingredientes.html', {'ingredientes': ingredientes})  # Rinde la plantilla de selección de ingredientes


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

def home_view(request):
    if 'usuario_id' in request.session:  # Verifica si el usuario ha iniciado sesión
        usuario_id = request.session['usuario_id']  # Obtiene el ID del usuario de la sesión
        historial_completo = []  # Lista para almacenar cada pedido con sus ingredientes y total

        pedidos = HistorialPedido.objects.filter(usuario_id=usuario_id)  # Obtiene todos los pedidos del usuario

        for pedido in pedidos:  # Itera sobre cada pedido
            ingredientes = pedido.pedidoingrediente_set.all()  # Obtiene los ingredientes relacionados con el pedido
            total_precio = pedido.calcular_total()  # Llama a la función para calcular el total del pedido
            historial_completo.append({
                'pedido': pedido,
                'ingredientes': ingredientes,
                'total_precio': total_precio
            })  # Agrega el pedido y sus detalles a la lista

        context = {
            'historial_completo': historial_completo  # Pasa el historial completo a la plantilla
        }
    else:
        context = {}  # Si no hay usuario autenticado, el contexto está vacío

    return render(request, 'home.html', context)  # Rinde la plantilla `home.html` con el contexto


def eliminar_historial_view(request):
    usuario_id = request.session.get('usuario_id')  # Obtiene el ID del usuario de la sesión
    if usuario_id:  # Verifica si el usuario ha iniciado sesión
        HistorialPedido.objects.filter(usuario_id=usuario_id).delete()  # Elimina todos los pedidos del usuario
        messages.success(request, "Historial de pedidos eliminado correctamente.")  # Muestra un mensaje de éxito
    else:
        messages.error(request, "Debes iniciar sesión para eliminar tu historial.")  # Muestra un mensaje de error si no hay usuario autenticado
    return redirect('home')  # Redirige a la página de inicio
