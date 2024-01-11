import cv2
import mediapipe as mp
import numpy as np
import time



# Tipagem =========================

confidence = float
webcam_image = np.ndarray
rgb_tuple = tuple[int, int, int]
coords_vector = int


# Classe =========================

class Detector:
    def __init__(self,
                 mode: bool = False,
                 number_hands: int = 2,
                 model_complexity: int = 1,
                 min_detec_confidence: confidence = 0.5,
                 min_tracking_confidence: confidence = 0.5):
        
        # Parametros para inicializar o hands
        self.mode = mode
        self.max_num_hands = number_hands
        self.complexity = model_complexity
        self.detection_con = min_detec_confidence
        self.tracking_con = min_tracking_confidence


        #inicializar o Hands
        self.mp_hands = mp.solutions.hands
        self.hands = self.mp_hands.Hands(self.mode,
                                         self.max_num_hands,
                                         self.complexity,
                                         self.detection_con,
                                         self.tracking_con)
        self.mp_draw = mp.solutions.drawing_utils
        self.tip_ids = [4,8,12,16,20]

    def find_hands(self,
                   img: webcam_image,
                   draw_hands: bool = True):
        
        # Correção de cor
        img_RGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

        # Coletar resultados do processo das hands e analisar
        self.results = self.hands.process(img_RGB)

        """ if self.results.multi_hand_landmarks and draw_hands:
            for hand in self.results.multi_hand_landmarks:
                self.mp_draw.draw_landmarks(img, hand, self.mp_hands.HAND_CONNECTIONS) """
        
        return img
    
    def find_position(self,
                      img: webcam_image,
                      hand_number: int = 0):
                
        self.required_landmark_list = []
        
        # my_hand = None   (só serviu para o Teste1 find_position)
        
        if self.results.multi_hand_landmarks:
            height, width, _ = img.shape 
            my_hand = self.results.multi_hand_landmarks[hand_number]
            for id, lm in enumerate(my_hand.landmark):
                center_x, center_y = int(lm.x * width), int(lm.y * height)

                self.required_landmark_list.append([id, center_x, center_y])

        return self.required_landmark_list
    
    def draw_in_position(self,
                         img: webcam_image,
                         x_vector: coords_vector,
                         y_vector: coords_vector,
                         rgb_selection: tuple = (255,0,0),
                         thickness: int = 10):
        x_vector = x_vector if type(x_vector) == list else [x_vector]
        y_vector = y_vector if type(y_vector) == list else [y_vector]

        for x, y in zip(x_vector, y_vector):
            cv2.circle(img, (x,y), thickness, rgb_selection, cv2.FILLED)
        
        return img







# Teste de Classe =========================
        
if __name__ == '__main__':
    # Declara a classe
    Detec = Detector()

    # Coletando o frame rate
    previous_time = 0
    current_time = 0

    capture = cv2.VideoCapture(0)
    while True:
        # Captura de imagem
        #cature.read retorna dois valores: sucess, img   - porém só usaremos o img
        _, img = capture.read()

        # Manipulação de frame
        img = Detec.find_hands(img)
        landmark_list = Detec.find_position(img)
        if landmark_list:
            print(landmark_list[8])     # O valor 8 indica o index do dedo desejado a trackear, neste caso o indicador.
        
        # Calculando o FPS
        current_time = time.time()
        fps = 1 / (current_time - previous_time)
        previous_time = current_time

        # Mostrando o frame
        cv2.putText(img, str(int(fps)), (10,70), cv2.FONT_HERSHEY_DUPLEX, 2, (255,0,255), 3)
        cv2.imshow('Camera', img)

        # Teste1 find_position
        #teste = Detec.find_position(img)
        #print(teste)

        # Quit app
        if cv2.waitKey(20) & 0xFF==ord('q'):            # q para encerrar o app
            break

