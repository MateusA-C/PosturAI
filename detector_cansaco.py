from scipy.spatial import distance  #Método para calcular a distância euclidiana 
import numpy as np
import cv2 as cv
import mediapipe as mp
from tkinter import messagebox
from detector_olhos_e_boca import DetectorOlhosEBoca
import logging
import time

class DetectorCansaco(DetectorOlhosEBoca):
    
    def __init__(self):

        super().__init__()
        self._boca = [78, 81, 13, 311, 308, 402, 14, 178]
        self._olho_esquerdo = [33, 160, 158, 133, 153, 144]
        self._olho_direito = [362, 385, 387, 263, 373, 380]
        self.frame_counter = 0
        self.score_de_fadiga = 0
        self.ear_treshold = 0.18
        self.ear_consec_frames = 40
        self.mar_treshold = 0.85

    def loop_captura(self):
        
        while True:

            ret,frame = self.cap.read()

            if not ret:

                logging.error("Ocorreu um erro ao capturar um frame")
                return
            
            frame_mostrar = frame.copy()
            ear_left_result = None
            ear_right_result = None
            mar_result = None

            timestamp = int(time.time()*1000)
            frame_rgb = cv.cvtColor(frame,cv.COLOR_BGR2RGB)
            mp_image = mp.Image(image_format=mp.ImageFormat.SRGB,data=frame_rgb)
            self._face_mesh.detect_async(mp_image,timestamp)
            if self.ultimo_resultado is not None:

                frame_mostrar = self.desenhar_landmarks(frame, self.ultimo_resultado)
                ear_left_result = self.eye_aspect_ratio(frame,self.ultimo_resultado,self._olho_esquerdo)
                ear_right_result = self.eye_aspect_ratio(frame,self.ultimo_resultado,self._olho_direito)
                mar_result = self.mouth_aspect_ratio(frame,self.ultimo_resultado)

            cv.imshow('frame_mostrar',frame_mostrar)

            if ear_left_result and ear_right_result and mar_result:

                ear_avg = (ear_left_result+ear_right_result)/2
                if ear_avg < self.ear_treshold:

                    self.frame_counter += 1

                    if self.frame_counter > self.ear_consec_frames:

                        self.score_de_fadiga += 1
                        logging.info("O usuário está fadigado!")
                        print(self.score_de_fadiga)
                        #messagebox.showinfo("Usuário cansado","Você parece cansado, por que não da uma pausa...")

                if mar_result > self.mar_treshold:

                    self.score_de_fadiga += 1
                    logging.info("O usuário está fadigado!")
                    print(self.score_de_fadiga)
                    #messagebox.showinfo("Usuário cansado","Você parece cansado, por que não da uma pausa...")
            
            if self.score_de_fadiga > 40:
                messagebox.showinfo("Usuário cansado","Você parece cansado, por que não da uma pausa...")
                self.score_de_fadiga = 0

            if cv.waitKey(1) == 27:
                
                logging.info("Você interrompeu a execução")
                break
            
        self.cap.release()
        cv.destroyAllWindows()

    def eye_aspect_ratio(self,frame,resultado,eye_indicies):

        pontos = list()
        if not resultado.face_landmarks:
            return 0.0

        h,w,_ = frame.shape
        rosto = resultado.face_landmarks[0]
        for item in eye_indicies:
            ponto = rosto[item]
            pontos.append((ponto.x*w,ponto.y*h))

        
        A = distance.euclidean(pontos[1],pontos[5])
        B = distance.euclidean(pontos[2],pontos[4])
        C = distance.euclidean(pontos[0],pontos[3])

        ear = (A+B)/(2.0*C)
        return ear
        
    def mouth_aspect_ratio(self,frame,resultado):

        pontos = list()
        if not resultado.face_landmarks:
            return 0.0
        
        h,w,_ = frame.shape
        rosto = resultado.face_landmarks[0]
        for item in self._boca:
            ponto = rosto[item]
            pontos.append((ponto.x*w,ponto.y*h))

        A = distance.euclidean(pontos[2], pontos[6])
        B = distance.euclidean(pontos[3], pontos[7])
        C = distance.euclidean(pontos[0], pontos[4])
        return (A + B) / (2.0 * C)
        

meu_detector = DetectorCansaco()
meu_detector.loop_captura()