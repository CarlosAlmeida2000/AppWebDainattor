import base64
import cv2
import numpy as np

class Image:
    
    def __init__(self):
        self.nombre_file = 'archivo'
    
    def get_file(self, base64_valor):
        try:
            decoded_data = base64.b64decode(base64_valor.split(',')[1])
            np_data = np.fromstring(decoded_data, np.uint8)
            img = cv2.imdecode(np_data, cv2.IMREAD_UNCHANGED)
            return img
        except Exception as e:
            return None
    
    def get_base64(self, array_foto):
        try:
            encoded_string = 'data:image/PNG;base64,' + str(base64.b64encode(array_foto))[2:][:-1]
            return encoded_string
        except Exception as e:
            return None