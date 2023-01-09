from .entrenamiento_facial import EntrenamientoFacial
from django.shortcuts import render, redirect
from django.http import JsonResponse
from .image import Image

entrenamiento_facial = EntrenamientoFacial()

# Create your views here.
# Vista para renderizar la plantilla de index
def vwConfiguracion(request):
    # Si no existe usuario autenticado, se lo redirecciona al login
    if not request.session.get('usuarioId'):
        return redirect('/')
    return render(request, 'configuracion.html')

def vwCaptRostroEntrena(request):
    try:
        if request.method == 'POST':
            img = Image()
            imagen_file = img.get_file(request.POST['imagen'][5:])
            result, tiene_rostro = entrenamiento_facial.capturar(request.session['usuarioId'], imagen_file, request.POST['cont_imagenes'])
            return JsonResponse({'result': result, 'tiene_rostro': tiene_rostro})
    except Exception as e:
        return JsonResponse({'result': '0'})

# Vista para renderizar la plantilla de index
def vwHistorial(request):
    # Si no existe usuario autenticado, se lo redirecciona al login
    if not request.session.get('usuarioId'):
        return redirect('/')
    return render(request, 'historial.html')

# Vista para renderizar la plantilla de index
def vwRecomendaciones(request):
    # Si no existe usuario autenticado, se lo redirecciona al login
    if not request.session.get('usuarioId'):
        return redirect('/')
    return render(request, 'recomendaciones.html')