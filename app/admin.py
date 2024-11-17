<<<<<<< Updated upstream
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
=======

from django.contrib import admin
from django.db.models import Sum
from django.db.models.functions import Coalesce
from django.db.models import DecimalField
from datetime import datetime
from .models import HistorialPedido, PedidoIngrediente, Ingrediente

# Admin para Ingrediente (como estaba antes)
class IngredienteAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'tipo', 'precio', 'disponible')
    list_editable = ('precio',)

# Admin para Ganancias (ya definida previamente)
class GananciasAdmin(admin.ModelAdmin):
    change_list_template = "admin/ganancias_change_list.html"
    
    def ganancias_totales(self, request):
        mes_actual = datetime.now().month
        anio_actual = datetime.now().year
        total_ganancias = HistorialPedido.objects.filter(
            fecha_pedido__month=mes_actual,
            fecha_pedido__year=anio_actual
        ).annotate(
            total_precio=Coalesce(Sum('pedidoingrediente__ingrediente__precio'), 0, output_field=DecimalField())
        )
        ganancias = sum(pedido.total_precio for pedido in total_ganancias)
        return ganancias

    def changelist_view(self, request, extra_context=None):
        ganancias = self.ganancias_totales(request)
        extra_context = extra_context or {}
        extra_context['ganancias_totales'] = ganancias
        return super().changelist_view(request, extra_context=extra_context)

# Registrar ambos administradores en el sitio admin
admin.site.register(Ingrediente, IngredienteAdmin)
admin.site.register(HistorialPedido, GananciasAdmin)

>>>>>>> Stashed changes
