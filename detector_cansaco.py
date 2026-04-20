from scipy.spatial import distance  #Método para calcular a distância euclidiana
import numpy as np  #Biblioteca numpy para poder trabalhar melhor com arrays e suas operações
import cv2 as cv  #Biblioteca opencv que será o nosso principal módulo de visão computacional
import mediapipe as mp  #biblioteca mediapipe que será o nosso módulo de inteligência artificial para detecção facial
from tkinter import messagebox
from detector_olhos_e_boca import DetectorOlhosEBoca
import logging
import time
from Notificacao import NotificacaoPosturAI

class DetectorCansaco(DetectorOlhosEBoca):
   
    def __init__(self):

        super().__init__()
        self.meu_notificador = NotificacaoPosturAI()

        # --- Configurações de Distância ---
        self.FOCAL_LENGHT = 793 # Valor médio calibrado para webcams 720p
        self.DIST_REAL_OLHOS = 6.3 # Distância média entre olhos em cm
        self.DIST_MINIMA_TELA = 50 # Limite ergonômico em cm
        self.frame_counter_dist = 0 # Contador para não disparar alerta toda hora

        self._boca = [78, 81, 13, 311, 308, 402, 14, 178]  #pontos específicos do mediapipe onde está a boca
        self._olho_esquerdo = [33, 160, 158, 133, 153, 144]  #pontos específicos do mediapipe onde está o olho esquerdo
        self._olho_direito = [362, 385, 387, 263, 373, 380]  #pontos específicos do mediapipe onde está o olho direito
        self.frame_counter = 0  #Nessa variável será armazenado a quantidade de frames consecutivos em que o sistema identificou algum sinal de cansaço (piscada/bocejada)
        self.score_de_fadiga = 0  #Vezes em que o sistema de fato identificou um sinal de fatiga, ou seja, se o sistema pegar [self.ear_consec_frames = 40] frames consecutivos de cansaço ele envia um ponto de fatiga
        self.ear_treshold = 0.18  #Limite de EAR para o modelo identificar um olho fechado (varia de pessoa pra pessoa)
        self.ear_consec_frames = 40  #Limite de frames consecutivos em que o sistema pode identificar sinais para decidir se de fato pe um sinal de fatiga ou não
        self.mar_treshold = 0.85  #Limite de EAR para o modelo identificar um bocejo (varia de pessoa pra pessoa)

    def loop_captura(self):

        while True:

            ret,frame = self.cap.read()  #ret é uma variável booleana que indica se o opencv conseguiu capturar o frame e frame é o objeto do nosso frame (imagem)

            if not ret:
                logging.error("Ocorreu um erro ao capturar um frame")
                return
            
            frame_mostrar = frame.copy()  #simplesmente uma cópia do frame atual
            ear_left_result = None  #resultado do algoritmo EAR para o olho esquerdo no frame atual
            ear_right_result = None #resultado do algoritmo EAR para o olho direito no frame atual
            mar_result = None  #resultado do algoritmo EAR para a boca esquerdo no frame atual
            timestamp = int(time.time()*1000)
            frame_rgb = cv.cvtColor(frame,cv.COLOR_BGR2RGB)  #converte o frame de BGR para RGB (BGR TO RGB)
            mp_image = mp.Image(image_format=mp.ImageFormat.SRGB,data=frame_rgb)
            self._face_mesh.detect_async(mp_image,timestamp)

            if self.ultimo_resultado is not None:

                frame_mostrar = self.desenhar_landmarks(frame, self.ultimo_resultado)
                distancia = self.calcula_distancia_cm(frame, self.ultimo_resultado)
                
                if distancia > 0:
                    cv.putText(frame_mostrar,
                                f"Distancia: {distancia}cm",
                                (30, 30), 
                                cv.FONT_HERSHEY_SIMPLEX,
                                0.7,
                                (0, 255, 0), 2)
                    
                    if distancia < self.DIST_MINIMA_TELA:
                        self.frame_counter_dist += 1
                        if self.frame_counter_dist > 60: # Se ficar muito perto por ~2 segundos
                            self.meu_notificador.enviar_alerta(
                                titulo="Postura Incorreta! 📏", 
                                mensagem="Você está muito perto da tela. Afaste-se um pouco!"
                            )
                            self.frame_counter_dist = 0
                    else:
                        self.frame_counter_dist = 0

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

                else:
                   
                    self.frame_counter = 0

                if mar_result > self.mar_treshold:

                    self.score_de_fadiga += 1
                    logging.info("O usuário está fadigado!")
                    print(self.score_de_fadiga)
                    #messagebox.showinfo("Usuário cansado","Você parece cansado, por que não da uma pausa...")

            if self.score_de_fadiga > 40:

                self.meu_notificador.enviar_alerta(titulo="Alerta de fatiga!",mensagem="Você parece cansado, porque não dá uma pausa? 😉")
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
    
    def calcula_distancia_cm(self,frame,resultado):

        if not resultado.face_landmarks:
            return 0.0

        h, w, _ = frame.shape
        rosto = resultado.face_landmarks[0]

        # Pegamos os pontos centrais dos olhos (33 e 263)
        p1 = rosto[33]
        p2 = rosto[263]

        # Convertemos coordenadas normalizadas (0-1) para pixels
        p1_px = (p1.x * w, p1.y * h)
        p2_px = (p2.x * w, p2.y * h)

        # Distância Euclidiana em pixels entre os olhos
        d_pixels = distance.euclidean(p1_px, p2_px)

        if d_pixels == 0: return 0.0

        # Fórmula: Distância (cm) = (Largura Real * Distância Focal) / Largura em Pixels
        distancia_cm = (self.DIST_REAL_OLHOS * self.FOCAL_LENGHT) / d_pixels
        return round(distancia_cm, 2)


meu_detector = DetectorCansaco()
meu_detector.loop_captura()