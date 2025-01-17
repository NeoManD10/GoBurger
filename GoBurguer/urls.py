"""
URL configuration for GoBurguer project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from app.views import login_view, home, ingredientes_view, register_view, logout_view, historial_view, generar_boleta_pdf, anadir_a_carrito_view, vista_carrito_view, borrar_del_carrito_view, get_or_create_carrito, about_us_view
from app_2.views import generar_reset_code_view, verificar_reset_code_view, actualizar_contrasena_view
# Cambia 'app' al nombre correcto de tu aplicación

urlpatterns = [
    path('admin/', admin.site.urls),
    path('login/', login_view, name='login'), 
    path('', home, name='home'),  # Página principal
    path('ingredientes/', ingredientes_view, name='ingredientes'),
    path('register/', register_view, name='register'),  # Ruta para la página de registro
    path('logout/', logout_view, name='logout'),
    path('historial/', historial_view, name='historial'),
    path('carrito/', vista_carrito_view, name='carrito'),
    path('generar-reset-code/', generar_reset_code_view, name='generar-reset-code'),
    path('verificar-reset-code/', verificar_reset_code_view, name='verificar-reset-code'),
    path('actualizar-contrasena/', actualizar_contrasena_view, name='actualizar-contrasena'),
    path('generar-boleta/',generar_boleta_pdf, name='generar-boleta'),
    path('acerca-de-nosotros/',about_us_view, name='about_us'),
    path('añadir-a-carrito/',anadir_a_carrito_view,name='añadir_a_carrito'),
    path('borrar-del-carrito/<int:pedido_id>/',borrar_del_carrito_view,name='borrar-del-carrito'),
    path('get-or-create-carrito/',get_or_create_carrito,name='get_or_create_carrito'),

]
