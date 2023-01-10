from Persona.models import Usuarios
import os, cv2, imutils
import numpy as np

class EntrenamientoFacial:
    def __init__(self):
        self.ruta_rostros = 'media\\Perfiles\\img_entrenamiento'
        self.ruta_modelos = 'Monitoreo\\modelos_entrenados\\'
        self.clasificador_haar = cv2.CascadeClassifier('Monitoreo\\modelos_entrenados\\haarcascade_frontalface_default.xml')
    
    def capturar(self, usuario_id, imagen, cont_imagenes):
        try:
            os.makedirs(self.ruta_rostros + '\\' + str(usuario_id), exist_ok = True)    
            # se crean las 200 imágenes de la persona monitoreada para después entrenar el modelo de reconocimiento facial
            imagen =  imutils.resize(imagen, width = 640)
            gray = cv2.cvtColor(imagen, cv2.COLOR_BGR2GRAY)
            auxFrame = imagen.copy()
            rostros = self.clasificador_haar.detectMultiScale(gray, 1.3, 5)
            rostro = []
            for (x, y, w, h) in rostros:
                cv2.putText(imagen,'rostro detectado',(x, y - 5),1,1.3,(255, 255, 0), 1, cv2.LINE_AA)
                cv2.rectangle(imagen, (x, y),(x + w, y + h),(255, 255, 255), 2)
                rostro = auxFrame[y:y + h, x:x + w]
                rostro = cv2.resize(rostro,(150, 150),interpolation = cv2.INTER_CUBIC)
                cv2.imwrite(self.ruta_rostros + '\\' + str(usuario_id) + '/rotro_{}.png'.format(cont_imagenes), rostro)
            if cont_imagenes == '99':
                if(self.entrenar(usuario_id) == 'entrenado'):
                    return '1', '1'
                return '0', '0'    
            if len(rostro) > 0:
                return '1', '1'
            return '1', '0'
        except Exception as e: 
            return '0', '0'
    
    def entrenar(self, usuario_id):
        try:
            # entrenamiento del modelo con todas las imágenes
            etiquetas = []
            datos_rostros = []
            cont_etiquetas = 0
            lista_personas = os.listdir(self.ruta_rostros)
            for persona in lista_personas:
                directorio_persona = self.ruta_rostros + '\\' + persona
                for archivo_foto in os.listdir(directorio_persona):
                    etiquetas.append(cont_etiquetas)
                    datos_rostros.append(cv2.imread(directorio_persona+'\\' + str(archivo_foto), 0))
                cont_etiquetas += 1
            reconocedor_facial = cv2.face.LBPHFaceRecognizer_create()
            reconocedor_facial.train(datos_rostros, np.array(etiquetas)) 
            reconocedor_facial.write(self.ruta_modelos + 'reconocedor_facial.xml')
            usuario = Usuarios.objects.get(pk = usuario_id)
            usuario.entrenamiento_facial = True
            usuario.save()
            print("Modelo de reconocimiento facial almacenado...")
            return 'entrenado'
        except Usuarios.DoesNotExist:
            return 'error'
        except Exception as e: 
            return 'error'