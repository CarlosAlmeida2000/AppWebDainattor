from django.db import models
from django.db.models import Q
from Persona.models import Usuarios
from random import sample
import numpy as np

# Create your models here.
class Actividades(models.Model):
    nombre = models.CharField(max_length = 120)
class Historial(models.Model):
    fecha_hora = models.DateTimeField()
    dia = models.IntegerField()
    imagen_expresion = models.ImageField(upload_to = 'Expresiones_detectadas', null = True, blank = True)
    expresion_facial = models.CharField(max_length = 15)
    usuario = models.ForeignKey('Persona.Usuarios', on_delete = models.PROTECT, related_name = "historial_usuario")

    @staticmethod
    def obtener_grafico(usuario_id):
        try:
            historial_grafico = []
            usuario = Usuarios.objects.get(pk = usuario_id)
            historial = usuario.historial_usuario.all().values()
            if (len(historial)):
                cantidad_actividades = 5
                actividades_recomen = []
                actividades_models = Actividades.objects.all()
                acti_aleatorias = sample([x for x in range(1, len(actividades_models))], cantidad_actividades)
                for i in range(cantidad_actividades):
                    actividades_recomen.append(actividades_models.get(pk = acti_aleatorias[i]).nombre)

                total_dias = historial.order_by('-dia')[0]['dia']
                # Si existe una semana de registro del historial, se predice el trastorno
                prediccion = Historial.prediccion_trastorno(total_dias, historial)

                object_json =  { 
                'dias_historial': total_dias,
                'enfadado': (historial.filter(expresion_facial = 'Enfadado').count()),
                'disgustado': (historial.filter(expresion_facial = 'Disgustado').count()),
                'temeroso': (historial.filter(expresion_facial = 'Temeroso').count()),
                'feliz': (historial.filter(expresion_facial = 'Feliz').count()),
                'neutral': (historial.filter(expresion_facial = 'Neutral').count()),
                'triste': (historial.filter(expresion_facial = 'Triste').count()),
                'sorprendido': (historial.filter(expresion_facial = 'Sorprendido').count()),
                'prediccion_trastorno': prediccion,
                'actividades': actividades_recomen
                }
                historial_grafico.append(object_json)
            return historial_grafico
        except Usuarios.DoesNotExist:    
            return []
        except Exception as e: 
            print(str(e))
            return []

    @staticmethod
    def prediccion_trastorno(total_dias, historial):
        emotion_dict = {0: 'Enfadado', 1: 'Disgustado', 2: 'Temeroso', 3: 'Feliz', 4: 'Neutral', 5: 'Triste', 6: 'Sorprendido'}
        frecuencia_enfadado = list()
        frecuencia_disgustado = list()
        frecuencia_temeroso = list()
        frecuencia_feliz = list()
        frecuencia_neutral = list()
        frecuencia_triste = list()
        frecuencia_sorprendido = list()
        dias_historial = list()
        predicciones_expresion = list()

        dias_historial = [(i + 1) for i in range(total_dias)]

        for d in dias_historial:
            frecuencia_enfadado.append(historial.filter(Q(dia = d) & Q(expresion_facial = 'Enfadado')).count())
            frecuencia_disgustado.append(historial.filter(Q(dia = d) & Q(expresion_facial = 'Disgustado')).count())
            frecuencia_temeroso.append(historial.filter(Q(dia = d) & Q(expresion_facial = 'Temeroso')).count())
            frecuencia_feliz.append(historial.filter(Q(dia = d) & Q(expresion_facial = 'Feliz')).count())
            frecuencia_neutral.append(historial.filter(Q(dia = d) & Q(expresion_facial = 'Neutral')).count())
            frecuencia_triste.append(historial.filter(Q(dia = d) & Q(expresion_facial = 'Triste')).count())
            frecuencia_sorprendido.append(historial.filter(Q(dia = d) & Q(expresion_facial = 'Sorprendido')).count())
        
        print('Enfadado: ', frecuencia_enfadado)
        print('Disgustado: ', frecuencia_disgustado)
        print('Temeroso:', frecuencia_temeroso)
        print('Feliz: ', frecuencia_feliz)
        print('Neutral: ', frecuencia_neutral)
        print('Triste:', frecuencia_triste)
        print('Sorprendido: ', frecuencia_sorprendido)

        predicciones_expresion.append(Historial.regresion_polinomial(dias_historial, frecuencia_enfadado, (total_dias + 1)))
        predicciones_expresion.append(Historial.regresion_polinomial(dias_historial, frecuencia_disgustado, (total_dias + 1)))
        predicciones_expresion.append(Historial.regresion_polinomial(dias_historial, frecuencia_temeroso, (total_dias + 1)))
        predicciones_expresion.append(Historial.regresion_polinomial(dias_historial, frecuencia_feliz, (total_dias + 1)))
        predicciones_expresion.append(Historial.regresion_polinomial(dias_historial, frecuencia_neutral, (total_dias + 1)))
        predicciones_expresion.append(Historial.regresion_polinomial(dias_historial, frecuencia_triste, (total_dias + 1)))
        predicciones_expresion.append(Historial.regresion_polinomial(dias_historial, frecuencia_sorprendido, (total_dias + 1)))

        print('prediciones de cada expresión: ', predicciones_expresion, '\n') 

        maxima_prediccion = max(predicciones_expresion)
        expresion_predecida = emotion_dict[predicciones_expresion.index(maxima_prediccion)]
        
        if expresion_predecida == 'Enfadado':
            return 'Se predice un posible Trastorno explosivo intermitente, se estima que a futuro se presente {0} veces la expresión de enfadado.'.format(int(round(maxima_prediccion, 2)))
        elif expresion_predecida == 'Disgustado':
            return 'Se predice un posible Trastorno obsesivo-compulsivo, se estima que a futuro se presente {0} veces la expresión de disgustado'.format(int(round(maxima_prediccion, 2)))
        elif expresion_predecida == 'Temeroso':
            return 'Se predice un posible Trastorno de la personalidad, se estima que a futuro se presente {0} veces la expresión de temeroso.'.format(int(round(maxima_prediccion, 2)))
        elif expresion_predecida == 'Triste':
            return 'Se predice un posible Trastorno depresivo, se estima que a futuro se presente {0} veces la expresión de triste.'.format(int(round(maxima_prediccion, 2)))
        elif expresion_predecida == 'Feliz' or expresion_predecida == 'Neutral' or expresion_predecida == 'Sorprendido':
            return 'No presenta ningún trastorno emocional.'

    @staticmethod
    def regresion_polinomial(x_train, y_train, x_prediction):
        # polinomio de grado 3
        modelo = np.poly1d(np.polyfit(x_train, y_train, 3))
        resultado_y = 0
        print(x_prediction)
        print("Ecuación polinómica: \n", modelo)
        resultado_y = ((modelo[3] * (x_prediction ** 3)) + (modelo[2] * (x_prediction ** 2)) + (modelo[1] * (x_prediction ** 1)) + modelo[0])
        return resultado_y