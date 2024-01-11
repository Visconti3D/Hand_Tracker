import cv2
import mediapipe as mp
import numpy as np
import math
import time

# Biblioteca que Permitem o Controle do Volume
import pycam
from ctypes import cast, POINTER
from comtypes import CLSCTX_ALL
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume

from hand_tracker import Detector

capture = cv2.VideoCapture(0)

# Configuração do CODEC de Video e Resolução
capture.set(cv2.CAP_PROP_FOURCC, cv2.VideoWriter_fourcc('M', 'J', 'P', 'G'))
cam_width = 1280
cam_height = 720
capture.set(cv2.CAP_PROP_FRAME_WIDTH, cam_width)
capture.set(cv2.CAP_PROP_FRAME_HEIGHT, cam_height)

# Ativando o detector de mãos
hand_detector = Detector()


# Ajustar o pycaw
# https://github.com/AndreMiras/pycaw
devices = AudioUtilities.GetSpeakers()
interface = devices.Activate(IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
volume = cast(interface, POINTER(IAudioEndpointVolume))

vol = 0


while True:
        # Captura de imagem
        #cature.read retorna dois valores: sucess, img   - porém só usaremos o img
        _, img = capture.read()

        # Manipulação de frames
        img = hand_detector.find_hands(img)

        landmark_list = hand_detector.find_position(img)


        if landmark_list:
            #print(landmark_list[8], landmark_list[4])

            x1, y1 = landmark_list[4][1], landmark_list[4][2]
            x2, y2 = landmark_list[8][1], landmark_list[8][2]
            x3, y3 = landmark_list[12][1], landmark_list[12][2]
            dist = math.sqrt(((x2-x1)**2) + ((y2-y1)**2))
            dist_switch = math.sqrt(((x3-x2)**2) + ((y3-y2)**2))
            print(dist_switch)

            center_x = (x1 + x2) // 2
            center_y = (y1 + y2) // 2

            hand_range = [50, 300]
            vol = ((dist-hand_range[0]) / hand_range[1])

            if vol < 0: vol=0
            if vol > 1: vol=1
            
            if dist_switch < 50 :
                vol_bar = np.interp(dist, hand_range, [400,150])        # 400 e 150 são os limites Y do desenho da barra de volume
                vol_percent = np.interp(dist, hand_range, [0,100]) 

                volume.SetMasterVolumeLevelScalar(vol, None)
                volText = int(vol * 100)

                # Barra dinâmica de volume         
                cv2.rectangle(img, (50,int(vol_bar)), (85,400), (30,186,35), cv2.FILLED)

                # Desenho da barra de volume
                # (imagem, coord 1, coord 2, RGB, thickness)
                cv2.rectangle(img, (50,150), (85,400), (30,30,186), 3)

                # img = hand_detector.draw_in_position(img, [x1, x2, center_x], [y1, y2, center_y])
                cv2.putText(img, f"{int(volText)}%", (x2,y2), cv2.FONT_HERSHEY_DUPLEX, 1, (30,186,35), 3)

        
        # Exibição dos frames
        cv2.imshow('Camera', img)
        
        # Quit app
        if cv2.waitKey(20) & 0xFF==ord('q'):            # q para encerrar o app
            break