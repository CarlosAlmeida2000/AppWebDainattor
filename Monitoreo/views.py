from django.shortcuts import render

# Create your views here.
# Vista para renderizar la plantilla de index
def vwConfiguracion(request):
    # Si no existe usuario autenticado, se lo redirecciona al login
    #if not request.session.get('UsuarioID'):
    #    return redirect('/')
    return render(request, 'configuracion.html')

# Vista para renderizar la plantilla de index
def vwHistorial(request):
    # Si no existe usuario autenticado, se lo redirecciona al login
    #if not request.session.get('UsuarioID'):
    #    return redirect('/')
    return render(request, 'historial.html')

# Vista para renderizar la plantilla de index
def vwRecomendaciones(request):
    # Si no existe usuario autenticado, se lo redirecciona al login
    #if not request.session.get('UsuarioID'):
    #    return redirect('/')
    return render(request, 'recomendaciones.html')