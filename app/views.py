from django.contrib import messages
from django.shortcuts import render, redirect
from .forms import LoginForm, RegisterForm
from .models import Usuario, Ingrediente,HistorialPedido, PedidoIngrediente, HistorialPedido

def login_view(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            contrasena = form.cleaned_data['contrasena']
            try:
                usuario = Usuario.objects.get(email=email, contrasena=contrasena)
                request.session['usuario_id'] = usuario.id
                request.session['usuario_nombre'] = usuario.nombre  # Guardar el nombre en la sesión
                return redirect('home')  # Redirigir a la página de inicio
            except Usuario.DoesNotExist:
                form.add_error(None, "Email o contraseña incorrectos")
    else:
        form = LoginForm()
    return render(request, 'login.html', {'form': form})


def home(request):
    if 'usuario_id' in request.session:
        usuario_id = request.session['usuario_id']
        # Obtener el historial de pedidos para el usuario
        historial_completo = HistorialPedido.objects.filter(usuario_id=usuario_id).select_related('usuario')
        pedidos_con_ingredientes = []

        for pedido in historial_completo:
            ingredientes = PedidoIngrediente.objects.filter(pedido=pedido)
            pedidos_con_ingredientes.append({'pedido': pedido, 'ingredientes': ingredientes})

        return render(request, 'home.html', {
            'historial_completo': pedidos_con_ingredientes
        })
    else:
        # Si no hay un usuario autenticado, no mostrar el historial
        return render(request, 'home.html', {
            'historial_completo': None
        })

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
    ingredientes = Ingrediente.objects.all()
    
    if request.method == 'POST':
        # Obtener ingredientes seleccionados
        ingredientes_ids = request.POST.getlist('ingredientes')

        if len(ingredientes_ids) > 4:
            messages.error(request, "No puedes seleccionar más de 4 ingredientes.")
            return render(request, 'ingredientes.html', {'ingredientes': ingredientes})

        # Obtener el usuario de la sesión
        usuario_id = request.session.get('usuario_id')
        if not usuario_id:
            messages.error(request, "Debes iniciar sesión para hacer un pedido.")
            return redirect('login')

        # Crear un nuevo historial de pedido
        historial_pedido = HistorialPedido.objects.create(usuario_id=usuario_id)

        # Guardar los ingredientes seleccionados en el pedido
        for ingrediente_id in ingredientes_ids:
            ingrediente = Ingrediente.objects.get(id=ingrediente_id)
            PedidoIngrediente.objects.create(pedido=historial_pedido, ingrediente=ingrediente)

        messages.success(request, "Pedido realizado con éxito.")
        return redirect('carrito')  # Redirigir a una página de carrito donde se puede ver el resumen del pedido

    return render(request, 'ingredientes.html', {'ingredientes': ingredientes})


def logout_view(request):
    # Eliminar el nombre de usuario de la sesión
    if 'usuario_nombre' in request.session:
        del request.session['usuario_nombre']
    return redirect('home')  # Redirigir a la página principal

def seleccionar_ingredientes_view(request):
    ingredientes = Ingrediente.objects.filter(disponible=True)

    if request.method == 'POST':
        usuario_id = request.session.get('usuario_id')
        if not usuario_id:
            return redirect('login')  # Redirigir si el usuario no está autenticado

        # Crear un nuevo historial de pedido
        pedido = HistorialPedido.objects.create(usuario_id=usuario_id)

        ingredientes_seleccionados = request.POST.getlist('ingredientes')
        precio_total = 0

        for ingrediente_id in ingredientes_seleccionados:
            ingrediente = Ingrediente.objects.get(id=ingrediente_id)
            PedidoIngrediente.objects.create(pedido=pedido, ingrediente=ingrediente)
            precio_total += ingrediente.precio

        request.session['precio_total'] = precio_total  # Guardar el precio en la sesión

        return redirect('resumen_pedido')  # Redirigir al resumen del pedido

    return render(request, 'ingredientes.html', {'ingredientes': ingredientes})

def historial_view(request):
    usuario_id = request.session.get('usuario_id')
    if not usuario_id:
        messages.error(request, "Debes iniciar sesión para ver tu historial.")
        return redirect('login')

    # Obtener todos los pedidos del usuario
    historial_pedidos = HistorialPedido.objects.filter(usuario_id=usuario_id)
    
    return render(request, 'historial.html', {'historial_pedidos': historial_pedidos})

def carrito_view(request):
    # Obtener el último pedido del usuario
    usuario_id = request.session.get('usuario_id')
    historial_pedido = HistorialPedido.objects.filter(usuario_id=usuario_id).last()

    # Obtener los ingredientes del pedido
    ingredientes = PedidoIngrediente.objects.filter(pedido=historial_pedido)

    # Calcular el total del pedido
    total_precio = sum([ingrediente.ingrediente.precio for ingrediente in ingredientes])

    return render(request, 'carrito.html', {
        'ingredientes': ingredientes,
        'total_precio': total_precio
    })

def home_view(request):
    if 'usuario_id' in request.session:
        usuario_id = request.session['usuario_id']
        historial_completo = []
        
        # Obtener el historial de pedidos del usuario
        pedidos = HistorialPedido.objects.filter(usuario_id=usuario_id)
        
        for pedido in pedidos:
            ingredientes = pedido.pedidoingrediente_set.all()  # Usar la relación inversa
            total_precio = pedido.calcular_total()  # Usar el método calcular_total
            print(f'Total del pedido {pedido.id}: {total_precio}')  # Imprimir el total para verificar
            historial_completo.append({
                'pedido': pedido,
                'ingredientes': ingredientes,
                'total_precio': total_precio  # Total del pedido
            })
        
        context = {
            'historial_completo': historial_completo,
        }
    else:
        context = {}

    return render(request, 'home.html', context)


def eliminar_historial_view(request):
    usuario_id = request.session.get('usuario_id')
    if usuario_id:
        # Eliminar todos los pedidos del usuario
        HistorialPedido.objects.filter(usuario_id=usuario_id).delete()
        messages.success(request, "Historial de pedidos eliminado correctamente.")
    else:
        messages.error(request, "Debes iniciar sesión para eliminar tu historial.")
    return redirect('home')

