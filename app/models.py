from django.db import models

class Usuario(models.Model):
    nombre = models.CharField(max_length=100)
    email = models.EmailField(max_length=150, unique=True)
    contrasena = models.CharField(max_length=255)
    fecha_registro = models.DateTimeField(auto_now_add=True)
    reset_code = models.CharField(max_length=4, blank=True, null=True)

    def __str__(self):
        return self.nombre

class Ingrediente(models.Model):
    nombre = models.CharField(max_length=100)
    tipo = models.CharField(max_length=50)
    precio = models.DecimalField(max_digits=10, decimal_places=2)
    disponible = models.BooleanField(default=True)

    def __str__(self):
        return self.nombre

class HistorialPedido(models.Model):
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE)
    fecha_pedido = models.DateTimeField(auto_now_add=True)

    def calcular_total(self):
        total = sum(item.ingrediente.precio for item in self.pedidoingrediente_set.all())
        return total

    def __str__(self):
        return f'Pedido {self.id} de {self.usuario.nombre}'


class PedidoIngrediente(models.Model):
    pedido = models.ForeignKey(HistorialPedido, on_delete=models.CASCADE)
    ingrediente = models.ForeignKey(Ingrediente, on_delete=models.CASCADE)

    def __str__(self):
        return f'Ingrediente {self.ingrediente.nombre} en Pedido {self.pedido.id}'
    
class Carrito(models.Model):
    carrito_id = models.AutoField(primary_key=True)  # SERIAL PK en PostgreSQL
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE)  # SERIAL FK en PostgreSQL
    precio_total = models.DecimalField(max_digits=10, decimal_places=2)  # DECIMAL(10,2)
    hora_de_creacion = models.DateTimeField(auto_now_add=True)  # TIMESTAMP para la fecha de creación

    def __str__(self):
        return f'Carrito {self.carrito_id} del usuario {self.usuario.nombre}'
