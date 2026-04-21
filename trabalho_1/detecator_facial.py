import cv2 as cv
import mediapipe as mp
import logging
import time

class DetectorFacial:

    def __init__(self):

        self.ultimo_resultado = None
        self.frame = None
        logging.basicConfig(level=logging.DEBUG)
        self.cap = cv.VideoCapture(0)
        self._options = mp.tasks.vision.FaceLandmarkerOptions(
            base_options = mp.tasks.BaseOptions(model_asset_path='face_landmarker.task'),
            running_mode = mp.tasks.vision.RunningMode.LIVE_STREAM,
            result_callback = self.callback
        )
        self._face_mesh = mp.tasks.vision.FaceLandmarker.create_from_options(self._options)

    def desenhar_landmarks(self,frame,resultado):

        if not resultado.face_landmarks:
            return frame
        
        h,w,_ = frame.shape

        for rosto in resultado.face_landmarks:
            for landmark in rosto:
                x = int(landmark.x*w)
                y = int(landmark.y*h)
                cv.circle(frame,(x,y),1,(0,255,0),-1)

        return frame
    
    def loop_captura(self):

        while True:

            ret,frame = self.cap.read()

            if not ret:

                logging.error("Ocorreu um erro ao capturar um frame")
                return

            timestamp = int(time.time()*1000)
            frame_rgb = cv.cvtColor(frame,cv.COLOR_BGR2RGB)
            mp_image = mp.Image(image_format=mp.ImageFormat.SRGB,data=frame_rgb)
            self._face_mesh.detect_async(mp_image,timestamp)
            if self.ultimo_resultado is not None:
                frame = self.desenhar_landmarks(frame, self.ultimo_resultado)
            cv.imshow('frame',frame)

            if cv.waitKey(1) == 27:

                logging.info("Você interrompeu a execução")
                break
        
        self.cap.release()
        cv.destroyAllWindows()

    def callback(self,resultado,imagem,timestap):
        self.ultimo_resultado = resultado
        
    


