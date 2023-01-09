from tensorflow.keras.layers import Dense, Dropout, Flatten, Conv2D, MaxPooling2D
from tensorflow.keras.models import Sequential
from django.core.files.base import ContentFile
from Monitoreo.models import Historial
from Persona.models import Usuarios
from django.db.models import Q
from datetime import datetime
import numpy as np
import cv2
import os

class ExpresionFacial:
    def __init__(self):
        # atributos generales 
        self.dataTrained = 'media\\Perfiles\\img_entrenamiento'
        self.rutaModelos = 'Monitoreo\\modelos_entrenados\\'
        self.personasEntrenadas = []
        self.expresionFacial = ''
        self.imagenExpresion = None
        # Construcción de la red neuronal convolucional
        self.reconocedor_expresiones = Sequential()

        # ************** Capa de entrada
        # Capa convolucional 1 con ReLU-activation
        self.reconocedor_expresiones.add(Conv2D(32, kernel_size = (3, 3), activation='relu', input_shape = (48, 48, 1)))
        # Capa convolucional 2 con ReLU-activation + un max poling
        self.reconocedor_expresiones.add(Conv2D(64, kernel_size = (3, 3), activation='relu'))
        # MaxPooling2D: Operación de agrupación máxima (2 x 2) para datos espaciales 2D.
        self.reconocedor_expresiones.add(MaxPooling2D(pool_size = (2, 2)))
        # El abandono o función Dropout() se implementa fácilmente mediante la selección aleatoria de nodos que se abandonarán con una probabilidad dada 
        # (por ejemplo, 25 %) en cada ciclo de actualización de peso
        self.reconocedor_expresiones.add(Dropout(0.25))

        # ************** Capa oculta
        # Capa convolucional 3 con ReLU-activation + un max poling
        self.reconocedor_expresiones.add(Conv2D(128, kernel_size = (3, 3), activation = 'relu'))
        # MaxPooling2D: Operación de agrupación máxima (2 x 2) para datos espaciales 2D.
        self.reconocedor_expresiones.add(MaxPooling2D(pool_size = (2, 2)))
        # Capa convolucional 4 con ReLU-activation + un max poling
        self.reconocedor_expresiones.add(Conv2D(128, kernel_size = (3, 3), activation = 'relu'))
        # MaxPooling2D: Operación de agrupación máxima (2 x 2) para datos espaciales 2D.
        self.reconocedor_expresiones.add(MaxPooling2D(pool_size = (2, 2)))
        # El abandono o función Dropout() se implementa fácilmente mediante la selección aleatoria de nodos que se abandonarán con una probabilidad dada 
        # (por ejemplo, 25 %) en cada ciclo de actualización de peso
        self.reconocedor_expresiones.add(Dropout(0.25))

        # ************** Capa de salida
        self.reconocedor_expresiones.add(Flatten())
        # Primera capa Densa completamente conectada con ReLU-activation.
        self.reconocedor_expresiones.add(Dense(1024, activation = 'relu'))
        # El abandono o función Dropout() se implementa fácilmente mediante la selección aleatoria de nodos que se abandonarán con una probabilidad dada 
        # (por ejemplo, 50 %) en cada ciclo de actualización de peso
        self.reconocedor_expresiones.add(Dropout(0.5))
        # Última capa Densa totalmente conectada con activación de softmax
        self.reconocedor_expresiones.add(Dense(7, activation = 'softmax'))
        
        # evita el uso de openCL y los mensajes de registro innecesarios
        cv2.ocl.setUseOpenCL(False)
        # diccionario que asigna a cada etiqueta una emoción (orden alfabético)
        self.emotion_dict = {0: 'Enfadado', 1: 'Disgustado', 2: 'Temeroso', 3: 'Feliz', 4: 'Neutral', 5: 'Triste', 6: 'Sorprendido'}
        # cargar el clasificador de detección de rostros pre entrenado de OpenCV
        self.clasificador_haar = cv2.CascadeClassifier('Monitoreo\\modelos_entrenados\\haarcascade_frontalface_default.xml')
        # cargar el modelo entrenado para reconocer expresiones faciales
        self.reconocedor_expresiones.load_weights(self.rutaModelos + 'modelo_expresiones.h5')
        
    
    # se registra el historial de la persona
    def guardarHistorial(self, usuario_id):
        historial = Historial()
        historial.fecha_hora = datetime.now()
        ultimo_dia = 1
        ultimo_historial = Historial.objects.filter(usuario_id = usuario_id).order_by('-fecha_hora')
        if (len(ultimo_historial) > 0):
            fecha_historial = datetime.strptime(ultimo_historial[0].fecha_hora.strftime('%Y-%m-%d'), '%Y-%m-%d')
            ultimo_dia = ultimo_historial[0].dia
            # Si la fecha actual es mayor al último historial, significa que el historial a registrar es de un nuevo día
            if (datetime.strptime(datetime.now().strftime('%Y-%m-%d'), '%Y-%m-%d') > fecha_historial):
                ultimo_dia += 1
        historial.dia = ultimo_dia
        historial.expresion_facial = self.expresionFacial
        historial.usuario = Usuarios.objects.get(pk = usuario_id)
        frame_jpg = cv2.imencode('.png', cv2.resize(self.imagenExpresion,(450, 450),interpolation = cv2.INTER_CUBIC))
        file = ContentFile(frame_jpg[1])
        historial.imagen_expresion.save('usuario_id_' + str(usuario_id) + '_fecha_' + str(historial.fecha_hora) + '.png', file, save = True)
        historial.save()

    def reconocer(self, usuario_id, imagen):
        try:
            personas_desconocidas = 0
            # cargar el modelo para el reconocimiento facial: El reconocimiento facial se realiza mediante el clasificador de distancia y vecino más cercano
            self.face_recognizer = cv2.face.LBPHFaceRecognizer_create()
            self.face_recognizer.read(self.rutaModelos + 'reconocedor_facial.xml')
            # se obtine la lista de personas a entrenadas
            self.personasEntrenadas = os.listdir(self.dataTrained)
            # convertir en escala de grises la imagen
            gray = cv2.cvtColor(imagen, cv2.COLOR_BGR2GRAY)
            auxFrame = gray.copy()
            auxFrame_color = imagen.copy()
            # detectando rostros - encuentra la cascada haar para dibujar la caja delimitadora alrededor de la cara
            faces = self.clasificador_haar.detectMultiScale(gray, scaleFactor = 1.3, minNeighbors = 5)
            # recorriendo rostros 
            for (x, y, w, h) in faces:
                rostro = auxFrame[y:y + h, x:x + w]
                self.imagenExpresion = auxFrame_color[y:y + h, x:x + w]
                # reconocimiento facial
                rostro = cv2.resize(rostro, (150, 150), interpolation = cv2.INTER_CUBIC)
                persona_identif = self.face_recognizer.predict(rostro)
                # se verifica si es la persona
                if persona_identif[1] < 70:
                    usuario_id_reconocido = self.personasEntrenadas[persona_identif[0]]
                    if(str(usuario_id) == str(usuario_id_reconocido)):
                        self.expresiones_recono = {}
                        cropped_img = np.expand_dims(np.expand_dims(cv2.resize(rostro, (48, 48)), -1), 0)

                        for e in range(6):
                            # se reconoce la expresión facial
                            prediction = self.reconocedor_expresiones.predict(cropped_img)
                            expresion = self.emotion_dict[int(np.argmax(prediction))]

                            contador_expresion = 1
                            if self.expresiones_recono.get(usuario_id, -1) != -1:
                                if self.expresiones_recono.get(usuario_id, -1).get(expresion, -1) != -1:
                                    contador_expresion = self.expresiones_recono.get(usuario_id, -1).get(expresion, -1)
                                    contador_expresion += 1
                                    self.expresiones_recono[usuario_id][expresion] = contador_expresion
                                else:
                                    self.expresiones_recono.get(usuario_id, -1).update({expresion: 1})
                            else:
                                self.expresiones_recono = {usuario_id: {expresion: 1}}

                        emociones = self.expresiones_recono.get(usuario_id, -1)
                        self.expresionFacial = max(emociones, key = emociones.get)

                        # se verifica si la última expresión facial registrada en el historial es igual a la expresión facial actual detectada
                        ultimo_historial = (Historial.objects.filter(Q(usuario_id = usuario_id) & Q(expresion_facial = self.expresionFacial)).order_by('-fecha_hora'))
                        if(len(ultimo_historial) > 0):
                            self.guardarHistorial(usuario_id)
                        else:
                            self.guardarHistorial(usuario_id)
                    else:
                        personas_desconocidas += 1
                else:
                    personas_desconocidas += 1
            if(len(faces) == personas_desconocidas):
                return '1', '0', ''
            return '1', '1', self.expresionFacial	
        except Exception as e: 
            return '0', '0', ''