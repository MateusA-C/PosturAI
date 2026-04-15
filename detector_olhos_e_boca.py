from detecator_facial import DetectorFacial
import cv2 as cv

class DetectorOlhosEBoca(DetectorFacial):

    def __init__(self):

        super().__init__()
        self.__olho_esquerdo = [33, 7, 163, 144, 145, 153, 154, 155, 133, 173, 157, 158, 159, 160, 161, 246]
        self.__olho_direito = [362, 382, 381, 380, 374, 373, 390, 249, 263, 466, 388, 387, 386, 385, 384, 398]
        self.__boca = [61, 146, 91, 181, 84, 17, 314, 405, 321, 375, 291, 308, 324, 318, 402, 317, 14, 87, 178, 88, 95]
        self.__regioes = {
            'olho esquerdo': (self.__olho_esquerdo,(0,255,0)), #Marca os pontos do olho esquerdo em verde
            'olho direito': (self.__olho_direito,(0,255,0)),   #Marca os pontos do olho direito em verde
            'boca': (self.__boca,(255,0,0))   #Marca os pontos da boca em vermelho
        }

    #Irei usar polimorfismo no método desenhar landmarks pra ele desenhar apenas os olhos e a boca
    def desenhar_landmarks(self, frame, resultado):

        if not resultado.face_landmarks:
            return frame

        h,w,_ = frame.shape

        for rosto in resultado.face_landmarks:
            for regiao,(indicies,cor) in self.__regioes.items():
                for i in indicies:
                    landmark = rosto[i]
                    x = int(landmark.x*w)
                    y = int(landmark.y *h)
                    cv.circle(frame,(x,y),2,cor,-1)

        return frame
    


