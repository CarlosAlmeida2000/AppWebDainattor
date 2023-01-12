import Monitoreo
from .entrenamiento_facial import EntrenamientoFacial
from django.shortcuts import render, redirect
from .reconocimiento import ExpresionFacial
from Monitoreo.models import Historial
from django.http import JsonResponse
from Persona.models import Usuarios
from django.db.models import Q
from .image import Image
import datetime

entrenamiento_facial = EntrenamientoFacial()
expresion = ExpresionFacial()

# Create your views here.
# Vista para renderizar la plantilla de index
def vwConfiguracion(request):
    # Si no existe usuario autenticado, se lo redirecciona al login
    if not request.session.get('usuarioId'):
        return redirect('/')
    return render(request, 'configuracion.html', {'configuracion': 'activate-menu'})

# Vista que guardar una foto para el entrenamiento facial
def vwCaptRostroEntrena(request):
    try:
        if request.method == 'POST':
            img = Image()
            imagen_file = img.get_file(request.POST['imagen'][5:])
            result, tiene_rostro = entrenamiento_facial.capturar(request.session['usuarioId'], imagen_file, request.POST['cont_imagenes'])
            return JsonResponse({'result': result, 'tiene_rostro': tiene_rostro})
    except Exception as e:
        return JsonResponse({'result': '0'})

# Vista que analiza la expresión facial de una imagen
def vwMonitorearExpre(request):
    try:
        if request.method == 'POST':
            img = Image()
            imagen_file = img.get_file(request.POST['imagen'][5:])
            result, tiene_rostro, expresion_facial = expresion.reconocer(request.session['usuarioId'], imagen_file)
            return JsonResponse({'result': result, 'tiene_rostro': tiene_rostro, 'expresion_facial': expresion_facial})
    except Exception as e:
        return JsonResponse({'result': '0'})

# Vista para renderizar la plantilla de historial
def vwHistorial(request):
    # Si no existe usuario autenticado, se lo redirecciona al login
    if not request.session.get('usuarioId'):
        return redirect('/')
    historial = Historial.objects.filter(usuario_id = request.session.get('usuarioId'))
    return render(request, 'historial.html', {'historial': historial, 'opc_historial': 'activate-menu'})

# Vista para filtrar historial de monitoreo
def vwBuscarHistorial(request):
    # Si no existe usuario autenticado, se lo redirecciona al login
    if not request.session.get('usuarioId'):
        return redirect('/')
    fecha = datetime.datetime.strptime(request.POST['dtmFechaHistorial'], "%Y-%m-%d").date() + datetime.timedelta(days = 1)
    if request.POST['expresion-facial'] == 'Todas':
        historial = Historial.objects.filter(Q(usuario_id = request.session.get('usuarioId')) & Q(fecha_hora__lte = fecha))
    else:
        historial = Historial.objects.filter(Q(usuario_id = request.session.get('usuarioId')) & Q(expresion_facial = request.POST['expresion-facial']) & Q(fecha_hora__lte = fecha))
    return render(request, 'historial.html', {'historial': historial, 'expresionSelected': request.POST['expresion-facial'], 'fechaSeleccionada': request.POST['dtmFechaHistorial'], 'opc_historial': 'activate-menu'})

# Vista para renderizar la plantilla de recomendaciones
def vwReporte(request):
    # Si no existe usuario autenticado, se lo redirecciona al login
    if not request.session.get('usuarioId'):
        return redirect('/')
    return render(request, 'reporte.html', {'reporte': 'activate-menu'})

# Vista que retorna los datos para el gráfico en barra
def vwGrafico(request):
    try:
        grafico = Historial.obtener_grafico(request.session.get('usuarioId'))
        return JsonResponse({'result': '1', 'grafico': grafico})
    except Exception as e:
        return JsonResponse({'result': '0'})