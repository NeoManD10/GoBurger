from django.contrib import admin
from django.urls import path
from app.views import login_view, home, ingredientes_view, register_view, logout_view , historial_view,carrito_view# Cambia 'app' al nombre correcto de tu aplicación

urlpatterns = [
    path('admin/', admin.site.urls),
    path('login/', login_view, name='login'), 
    path('', home, name='home'),  # Página principal
    path('ingredientes/', ingredientes_view, name='ingredientes'),
    path('register/', register_view, name='register'),  # Ruta para la página de registro
    path('logout/', logout_view, name='logout'),
    path('historial/', historial_view, name='historial'),
    path('carrito/', carrito_view, name='carrito'), 

]

