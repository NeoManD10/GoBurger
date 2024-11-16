from django.contrib import admin
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
