from Persona.models import Usuarios, Personas
from django.shortcuts import render, redirect
from django.db import IntegrityError
from django.http import JsonResponse
from django.db import transaction
import hashlib
import os

# **********INICIO DE SESION********

# Vista para renderizar la plantilla de login
def vwInicio(request):
    return render(request, 'login.html')

# Vista para renderizar la plantilla de registro de usuario
def vwRegistro(request):
    return render(request, 'registro.html')

# Vista para renderizar la plantilla de index
def vwHome(request):
    # Si no existe usuario autenticado, se lo redirecciona al login
    if not request.session.get('usuarioId'):
        return redirect('/')
    return render(request, 'home.html')

# Vista para iniciar sesión
def IniciarSesion(request):
    try:
        if request.method == 'POST':
            usuario = request.POST['txtUsuario']
            unUsuario = Usuarios.objects.get(nom_usuario = usuario)
            if unUsuario:
                if unUsuario.clave == cifrar(request.POST['txtClave']):
                    request.session['usuarioId'] = unUsuario.id
                    request.session['personaId'] = unUsuario.persona.id
                    request.session['nombres'] = unUsuario.persona.nombres_apellidos
                    if unUsuario.persona.foto_perfil:
                        request.session['fotoPerfil'] = unUsuario.persona.foto_perfil.url
                    return JsonResponse({'result': '1'})
                return JsonResponse({'result': '2'})
            return JsonResponse({'result': '2'})
    except Usuarios.DoesNotExist:
        return JsonResponse({'result': '2'})
    except Exception as e:
        return JsonResponse({'result': '0'})

# Vista para cerrar sesión
def CerrarSesion(request):
    if request.session.get('usuarioId'):
        del request.session['usuarioId']
        del request.session['personaId']
        del request.session['nombres']
        if request.session.get('fotoPerfil'):
            del request.session['fotoPerfil']
        request.session.flush()
    return redirect('/')

# **********MODIFICAR PERFIL DE USUARIO********

# Vista para renderizar la plantilla de modificar perfil de usuario
def vwPerfil(request):
    # Si no existe usuario autenticado, se lo redirecciona al login
    if not request.session.get('usuarioId'):
        return redirect('/')
    try:
        unUsuario = Usuarios.objects.get(id = request.session['usuarioId'])
        unUsuario.persona.fecha_nacimiento = unUsuario.persona.fecha_nacimiento.strftime('%Y-%m-%d')
        return render(request, 'perfil.html', {'unUsuario': unUsuario, 'perfil': 'activate-menu'})
    except Usuarios.DoesNotExist:
        return JsonResponse({'result': '2'})
    except Exception as e:
        return JsonResponse({'result': '0'})

# Vista para añadir nuevos usuarios.
def vwGuardarUsuario(request):
    try:
        with transaction.atomic():
            if request.method == 'POST':
                existe_persona = Personas.objects.filter(cedula = request.POST['txtCedula'])
                if len(existe_persona) == 0:
                    unUsuario = Usuarios()
                    unUsuario.nom_usuario = request.POST['txtUsuario']
                    # En caso de no haber ingresado ninguna contraseña, se mantiene la actual.
                    if request.POST['txtClave']:
                        unUsuario.clave = cifrar(request.POST['txtClave'])
                    unaPersona = Personas()
                    unaPersona.nombres_apellidos = request.POST['txtNombres']
                    unaPersona.cedula = request.POST['txtCedula']
                    unaPersona.fecha_nacimiento = request.POST['dtmFechaNaci']
                    unaPersona.save()
                    unUsuario.persona = unaPersona
                    unUsuario.save()
                    # Actualizar la variable sesion de nombres de usuario.
                    request.session['nombres'] = unaPersona.nombres_apellidos
                    return JsonResponse({'result': '1'})
                else:
                    # Ingreso la cédula de otra persona ya registrada
                    return JsonResponse({'result': '3'})        
    except IntegrityError:
        # Usuario repetido
        return JsonResponse({'result': '4'})   
    except Exception as e:
        return JsonResponse({'result': '0'})

# Vista para realizar los cambios en los datos del usuario
def vwModificarUsuario(request):
    try:
        with transaction.atomic():
            if request.method == 'POST':
                unUsuario = Usuarios.objects.get(id = request.session['usuarioId'])
                existe_persona = Personas.objects.filter(cedula = request.POST['txtCedula'])
                if len(existe_persona) == 0 or (len(existe_persona) == 1 and existe_persona[0].id == unUsuario.persona.id):
                    unUsuario.nom_usuario = request.POST['txtUsuario']
                    # En caso de no haber ingresado ninguna contraseña, se mantiene la actual.
                    if request.POST['txtClave']:
                        unUsuario.clave = cifrar(request.POST['txtClave'])
                    unaPersona = Personas.objects.get(pk = unUsuario.persona.id)
                    unaPersona.nombres_apellidos = request.POST['txtNombres']
                    unaPersona.cedula = request.POST['txtCedula']
                    unaPersona.fecha_nacimiento = request.POST['dtmFechaNaci']
                    unaPersona.save()
                    unUsuario.save()
                    # Actualizar la variable sesion de nombres de usuario.
                    request.session['nombres'] = unaPersona.nombres_apellidos
                    return JsonResponse({'result': '1'})
                else:
                    # Ingreso la cédula de otra persona ya registrada
                    return JsonResponse({'result': '3'})    
    except IntegrityError:
        # Usuario repetido
        return JsonResponse({'result': '4'})    
    except Personas.DoesNotExist or Usuarios.DoesNotExist:
        return JsonResponse({'result': '2'})
    except Exception as e:
        return JsonResponse({'result': '0'})

# Vista para realizar cambio de foto de usuario
def vwModificarFotoUsuario(request):
    try:
        if request.method == 'POST':
            unaPersona = Personas.objects.get(pk = request.session['personaId'])
            imgborrar = unaPersona.foto_perfil.name
            try:
                unaPersona.foto_perfil = request.FILES['imgFoto']
                a, b = os.path.splitext(unaPersona.foto_perfil.name)
                unaPersona.foto_perfil.name = "img_persona_" + str(unaPersona.id) + b
                unaPersona.save()
                os.remove('media\\' + imgborrar)
            except Exception as e:
                pass
        # Actualizar la variable sesion de foto de usuario.
        request.session['fotoPerfil'] = '\\media\\' + unaPersona.foto_perfil.name
        return JsonResponse({'result': '1'})
    except Personas.DoesNotExist:
        return JsonResponse({'result': '2'})
    except Exception as e:
        return JsonResponse({'result': '0'})

# Función para cifrar contrasena
def cifrar(clave):
    h = hashlib.new('sha256')
    h.update(clave.encode())
    return h.hexdigest()