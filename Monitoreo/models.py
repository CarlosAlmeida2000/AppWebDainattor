from django.db import models
from django.db.models import Q, Value
from django.db.models.functions import Concat
from Persona.models import Usuarios
from Monitoreo.image import Image
from sklearn import linear_model

# Create your models here.

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
                # Si existe una semana de registro del historial, se predice el trastorno
                prediccion = 'Para la predicción del trastorno, debe tener 7 días de registros en el historial.'
                total_dias = historial.order_by('-dia')[0]['dia']
                if(total_dias > 1):
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
                'prediccion_trastorno': prediccion
                }
                historial_grafico.append(object_json)
            return historial_grafico
        except Usuarios.DoesNotExist:    
            return []
        except Exception as e: 
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
        predicciones_emocion = list()

        dias_historial = [[(i + 1)] for i in range(total_dias)]

        for d in dias_historial:
            frecuencia_enfadado.append(historial.filter(Q(dia = d[0]) & Q(expresion_facial = 'Enfadado')).count())
            frecuencia_disgustado.append(historial.filter(Q(dia = d[0]) & Q(expresion_facial = 'Disgustado')).count())
            frecuencia_temeroso.append(historial.filter(Q(dia = d[0]) & Q(expresion_facial = 'Temeroso')).count())
            frecuencia_feliz.append(historial.filter(Q(dia = d[0]) & Q(expresion_facial = 'Feliz')).count())
            frecuencia_neutral.append(historial.filter(Q(dia = d[0]) & Q(expresion_facial = 'Neutral')).count())
            frecuencia_triste.append(historial.filter(Q(dia = d[0]) & Q(expresion_facial = 'Triste')).count())
            frecuencia_sorprendido.append(historial.filter(Q(dia = d[0]) & Q(expresion_facial = 'Sorprendido')).count())
        
        print('Enfadado: ', frecuencia_enfadado)
        print('Disgustado: ', frecuencia_disgustado)
        print('Temeroso:', frecuencia_temeroso)
        print('Feliz: ', frecuencia_feliz)
        print('Neutral: ', frecuencia_neutral)
        print('Triste:', frecuencia_triste)
        print('Sorprendido: ', frecuencia_sorprendido)

        predicciones_emocion.append(Historial.regresion_logistica(dias_historial, frecuencia_enfadado, (total_dias + 1)))
        predicciones_emocion.append(Historial.regresion_logistica(dias_historial, frecuencia_disgustado, (total_dias + 1)))
        predicciones_emocion.append(Historial.regresion_logistica(dias_historial, frecuencia_temeroso, (total_dias + 1)))
        predicciones_emocion.append(Historial.regresion_logistica(dias_historial, frecuencia_feliz, (total_dias + 1)))
        predicciones_emocion.append(Historial.regresion_logistica(dias_historial, frecuencia_neutral, (total_dias + 1)))
        predicciones_emocion.append(Historial.regresion_logistica(dias_historial, frecuencia_triste, (total_dias + 1)))
        predicciones_emocion.append(Historial.regresion_logistica(dias_historial, frecuencia_sorprendido, (total_dias + 1)))

        print('prediciones de cada emoción: ', predicciones_emocion, '\n') 

        maxima_prediccion = max(predicciones_emocion)
        emocion_predecida = emotion_dict[predicciones_emocion.index(maxima_prediccion)]
        
        print(emocion_predecida, maxima_prediccion)
        if emocion_predecida == 'Enfadado':
            return 'Trastorno explosivo intermitente con una predicción de aparición futura de la emoción de enfadado de {0} veces.'.format(maxima_prediccion)
        elif emocion_predecida == 'Disgustado':
            return 'Trastorno obsesivo-compulsivo con una predicción de aparición futura de la emoción de disgustado de {0} veces'.format(maxima_prediccion)
        elif emocion_predecida == 'Temeroso':
            return 'Trastorno de la personalidad con predicción de aparición futura de la emoción temeroso de {0} veces'.format(maxima_prediccion)
        elif emocion_predecida == 'Triste':
            return 'Trastorno depresivo con una predicción de aparición futura de la emoción triste de {0} veces'.format(maxima_prediccion)
        elif emocion_predecida == 'Feliz' or emocion_predecida == 'Neutral' or emocion_predecida == 'Sorprendido':
            return 'Ningún trastorno'

    @staticmethod
    def regresion_logistica(x_train, y_train, x_prediction):
        # Creamos el objeto de Regresión Logística
        regresion = linear_model.LogisticRegression()
        # Entrenamos nuestro modelo
        regresion.fit(x_train, y_train) 
        # Predicción de ocurrencua de una emoción dado un día x
        return int(regresion.predict([[x_prediction]]))