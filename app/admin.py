# admin.py
from django.contrib import admin
<<<<<<< Updated upstream
<<<<<<< Updated upstream

# Register your models here.
=======
from .models import Ingrediente, PedidoIngrediente

class IngredienteAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'tipo', 'precio', 'cantidad', 'disponible', 'frecuencia')  # Añadimos 'disponible'
    list_editable = ('cantidad', 'precio', 'disponible')  # Hacemos editable 'disponible' además de cantidad y precio
    search_fields = ('nombre', 'tipo')
    list_filter = ('tipo',)

    # Función para mostrar la frecuencia de cada ingrediente
    def frecuencia(self, obj):
        # Contamos cuántas veces el ingrediente ha sido añadido en los pedidos
        return PedidoIngrediente.objects.filter(ingrediente=obj).count()
    frecuencia.short_description = 'Frecuencia'  # Título para la columna

# Registramos el modelo con su admin personalizado
admin.site.register(Ingrediente, IngredienteAdmin)

>>>>>>> Stashed changes
=======
from django.db.models import Count
from .models import Ingrediente, HistorialPedido, PedidoIngrediente

class IngredienteAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'tipo', 'precio', 'disponible', 'frecuencia_en_pedidos')

    # Función que cuenta la frecuencia de un ingrediente en los pedidos
    def frecuencia_en_pedidos(self, obj):
        # Contamos cuántos pedidos contienen este ingrediente
        return PedidoIngrediente.objects.filter(ingrediente=obj).count()

    frecuencia_en_pedidos.short_description = 'Frecuencia en Pedidos'

    # Opcional: Agregar filtros y búsqueda
    list_filter = ('tipo', 'disponible')
    search_fields = ('nombre',)

admin.site.register(Ingrediente, IngredienteAdmin)

>>>>>>> Stashed changes
