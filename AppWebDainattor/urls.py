"""AppWebDainattor URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
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
from Monitoreo import views as vwMonitoreo
from django.conf.urls.static import static
from Persona import views as vwPersona
from django.contrib import admin
from django.conf import settings
from django.urls import path


urlpatterns = [
    path('admin/', admin.site.urls),
    # Sección Persona
    path('', vwPersona.vwInicio),
    path('registro/', vwPersona.vwRegistro, name='registro'),
    path('perfil/', vwPersona.vwPerfil, name='perfil'),
    path('guardar-usuario/', vwPersona.vwGuardarUsuario, name='guardar-usuario'),
    path('login/', vwPersona.IniciarSesion, name='login'),
    path('home/', vwPersona.vwHome, name='home'),
    path('modificar-usuario/', vwPersona.vwModificarUsuario, name='modificar-usuario'),
    path('modificar-foto-usuario/', vwPersona.vwModificarFotoUsuario, name='modificar-foto-usuario'),
    path('logout/', vwPersona.CerrarSesion, name='logout'),
    # Sección de Monitoreo
    path('configuracion/', vwMonitoreo.vwConfiguracion, name='configuracion'),
    path('historial/', vwMonitoreo.vwHistorial, name='historial'),
    path('recomendaciones/', vwMonitoreo.vwRecomendaciones, name='recomendaciones'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT) + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

# Creando el acceso para los archivos de media
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)