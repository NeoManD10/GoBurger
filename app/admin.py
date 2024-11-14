from django.contrib import admin
from .models import Ingrediente

admin.site.register(Ingrediente)
# Register your models here.
class Ingrediente(admin.ModelAdmin):
    mostrar_lista = ('nombre', 'tipo', 'precio', 'disponible')
