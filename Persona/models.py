from fernet_fields import EncryptedTextField
from django.db import models

# Create your models here.
class Personas(models.Model):
    nombres_apellidos = models.CharField(max_length = 70)
    fecha_nacimiento = models.DateField()
    foto_perfil = models.ImageField(upload_to = 'Perfiles', null = True, blank = True)

class Usuarios(models.Model):
    nom_usuario = models.CharField(max_length = 20, unique = True)
    clave = EncryptedTextField()
    entrenamiento_facial = models.BooleanField(default =  False)
    persona = models.OneToOneField('Persona.Personas', on_delete = models.PROTECT, unique = True)