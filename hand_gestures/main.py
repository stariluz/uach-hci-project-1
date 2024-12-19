import cv2
import mediapipe as mp
import numpy as np
import math
import time
import pyautogui

# Configuraciones para el control de mouse
screen_w, screen_h = pyautogui.size()  # Obtener dimensiones de pantalla

# Variables para detección de eventos
clicks_counter = 0
click_down_time = None
is_in_click = False
click_timer = None
last_click_time = 0  # Tiempo del último clic registrado
double_click_timeout = 0.3  # Tiempo para considerar doble clic (300ms)
long_click_threshold = 0.5  # Tiempo mínimo para considerar un clic largo (500ms)

# MediaPipe y OpenCV setup
mpHands = mp.solutions.hands
Hands = mpHands.Hands()
mpDraw = mp.solutions.drawing_utils
PTime = 0

cap = cv2.VideoCapture(0)

while cap.isOpened():
    lmList = []
    success, img = cap.read()
    converted_image = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    results = Hands.process(converted_image)

    if results.multi_hand_landmarks:
        for hand_in_frame in results.multi_hand_landmarks:
            mpDraw.draw_landmarks(img, hand_in_frame, mpHands.HAND_CONNECTIONS)
        for id, lm in enumerate(results.multi_hand_landmarks[0].landmark):
            h, w, c = img.shape
            cx, cy = int(lm.x * w), int(lm.y * h)
            lmList.append([cx, cy])

        if len(lmList) != 0:
            x1, y1 = lmList[4][0], lmList[4][1]  # Pulgar
            x2, y2 = lmList[8][0], lmList[8][1]  # Índice
            # x_thumb_base, y_thumb_base = lmList[2][0], lmList[2][1]  # Pulgar base (landmark 2)

            # Invertir la coordenada X para que coincida con el movimiento en pantalla
            mouse_x = np.interp(x1, [0, w], [0, screen_w])  # Invertir rango de X
            mouse_x = screen_w - mouse_x  # Invertir el resultado para que el movimiento sea correcto

            mouse_y = np.interp(y2, [0, h], [0, screen_h])

            # Mover el mouse a la posición del dedo índice
            pyautogui.moveTo(mouse_x, mouse_y)

            # Dibujamos círculos en los puntos relevantes
            cv2.circle(img, (x1, y1), 15, (255, 0, 0), cv2.FILLED)
            cv2.circle(img, (x2, y2), 15, (255, 0, 0), cv2.FILLED)
            cv2.line(img, (x1, y1), (x2, y2), (255, 0, 0), 3, cv2.FILLED)

            # Calculamos la longitud entre el pulgar y el índice
            length = math.hypot(x2 - x1, y2 - y1)

            # Detectar "click down" (cuando comienza un clic)
            if length < 40:
                if not is_in_click:
                    click_down_time = time.time()
                    is_in_click = True
                    print("Click Down")
                    pyautogui.mouseDown()  # Simular mantener presionado el clic

            # Detectar "click up" (cuando el clic se suelta)
            elif is_in_click:
                click_duration = time.time() - click_down_time

                # Si la duración del clic es larga
                if click_duration >= long_click_threshold:
                    print("Long Click")
                    pyautogui.mouseUp()  # Soltar el clic
                else:
                    # Si ocurre dentro del tiempo para doble clic
                    if time.time() - last_click_time <= double_click_timeout:
                        clicks_counter += 1
                        print("Double Click")
                        pyautogui.mouseUp()  # Soltar el clic
                        pyautogui.doubleClick()  # Simular doble clic
                        last_click_time = 0  # Resetear temporizador
                    else:
                        clicks_counter += 1
                        print("Single Click")
                        pyautogui.mouseUp()  # Soltar el clic
                        pyautogui.click()  # Simular un solo clic
                    
                    last_click_time = time.time()  # Iniciar temporizador para el próximo clic

                is_in_click = False  # Finalizar clic
                print("Click Up")

    # Mostrar el contador de clics en la imagen
    cv2.putText(img, f'Clicks: {clicks_counter}', (450, 50), cv2.FONT_HERSHEY_COMPLEX, 1, (0, 255, 255), 3)

    # Mostrar FPS
    CTime = time.time()
    fps = 1 / (CTime - PTime)
    PTime = CTime
    cv2.putText(img, str(int(fps)), (40, 50), cv2.FONT_HERSHEY_COMPLEX, 1, (255, 0, 0), 3)

    # Mostrar la ventana de la cámara
    cv2.imshow("Hand Tracking", img)

    # Salir con la tecla 'Q'
    if cv2.waitKey(1) == 113:  # 113 es 'q'
        break

cap.release()
cv2.destroyAllWindows()