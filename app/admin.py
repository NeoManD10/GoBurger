from django.utils.html import format_html
from django.contrib import admin
from django.db.models import Sum
from django.db.models.functions import Coalesce
from django.db.models import DecimalField
from datetime import datetime
from .models import HistorialPedido, PedidoIngrediente, Ingrediente

# Admin para Ingrediente (como estaba antes)
class IngredienteAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'tipo', 'precio', 'disponible')  # Mostrar si está disponible
    list_editable = ('precio', 'disponible')  # Permitir edición en línea de 'precio' y 'disponible'
    search_fields = ('nombre', 'tipo')  # Habilitar barra de búsqueda
    list_filter = ('tipo', 'disponible')  # Filtros por tipo y disponibilidad
    ordering = ('tipo', 'nombre')  # Ordenar por tipo y nombre

    def disponibilidad_icono(self, obj):
        if obj.disponible:
            return format_html('<span style="color: green;">✔ Disponible</span>')
        return format_html('<span style="color: red;">✘ No Disponible</span>')
    disponibilidad_icono.short_description = 'Disponibilidad'


# Admin para Ganancias (ya definida previamente)
class GananciasAdmin(admin.ModelAdmin):
    change_list_template = "ganancias_change_list.html"
    
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