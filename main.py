#Hola, disfruten a los monitos ;)

import cv2          # maneja la camara, el procesamiento de imágenes y ventana de video realtime (Asegúrate de tener OpenCV instalado)
import numpy as np  # para manipulación datos en matrices
import os           # nódulo nativo para manejo de archivos y rutas

try: 
    from mediapipe.python.solutions import hands as mp_hands        # Detección de manos, asegurate de tener MediaPipe instalado: pip install mediapipe
    from mediapipe.python.solutions import drawing_utils as mp_draw # Dibuja los puntos de referencia de las manos
except ImportError:
    print("Error al importar mediapipe.")
    exit()

# DICCIONARIO DE RUTAS DE IMÁGENES PARA CADA GESTO
IMAGENES = {
    'mono hola':     'assets/hola.png',
    'mono cerrado':  'assets/punio.png',
    'mono pensando': 'assets/pensando.png',
    'mono idea':     'assets/idea.png',
    'mono sorpresa': 'assets/abierta.png',
}

# configuramos el detector de mediaPipe para soportar tracking de dos manos
detector = mp_hands.Hands(
    static_image_mode=False,
    max_num_hands=2,
    min_detection_confidence=0.7,
    min_tracking_confidence=0.7,
)

# carga y Control de Assets
def cargar_imagenes():
    """Carga las imágenes del diccionario y las escala para la interfaz."""
    imgs = {}
    for gesto, ruta in IMAGENES.items():
        img = cv2.imread(ruta) if os.path.exists(ruta) else None
        imgs[gesto] = cv2.resize(img, (300, 300)) if img is not None else crear_placeholder(gesto)
    return imgs

# Placeholder para gestos sin imagen
def crear_placeholder(gesto):
    """Crea un cuadro gris con texto por si el usuario no tiene los archivos de los monitos."""
    img = np.ones((300, 300, 3), dtype=np.uint8) * 40
    cv2.putText(img, gesto.upper(), (20, 155), cv2.FONT_HERSHEY_SIMPLEX, 0.65, (0, 255, 255), 2)
    return img

# ANÁLISIS DE GESTOS
def analizar_gestos(resultados):
    """Analiza la posición y los ángulos de los dedos para clasificar el gesto."""
    if not resultados.multi_hand_landmarks:
        return 'ninguno'
    
    def evaluar_mano(puntos):
        """Calcula cuántos dedos están abiertos usando distancias relativas e invariantes a la rotación."""
        def dist_sq(p1, p2):
            return (p1.x - p2.x)**2 + (p1.y - p2.y)**2
        
        muneca = puntos[0] #muñeca/wrist
        
        # Evaluamos si la punta del dedo está más lejos de la muñeca que su articulación media
        i  = dist_sq(puntos[8], muneca)  > dist_sq(puntos[6], muneca)   # Índice
        m  = dist_sq(puntos[12], muneca) > dist_sq(puntos[10], muneca)  # Medio
        a  = dist_sq(puntos[16], muneca) > dist_sq(puntos[14], muneca)  # Anular
        me = dist_sq(puntos[20], muneca) > dist_sq(puntos[18], muneca)  # Meñique
        # El pulgar se mide de forma lateral respecto al centro de la palma
        p  = dist_sq(puntos[4], puntos[9]) > dist_sq(puntos[2], puntos[9])

        total_abiertos = sum([i, m, a, me, p])
        return total_abiertos, i, m, a, me, p #Conteo de dedos desplegados

    #--------------------------------------------------------------
    # MONITO SORPRENDIDO DOS GESTOS (identificamos dos manos abiertas e inclinadas hacia la cabeza)
    #--------------------------------------------------------------
    if len(resultados.multi_hand_landmarks) == 2:
        # Ordenamos las manos por su coordenada X para identificar izquierda y derecha en pantalla
        manos_ordenadas = sorted(resultados.multi_hand_landmarks, key=lambda h: h.landmark[0].x)
        m_izq = manos_ordenadas[0].landmark
        m_der = manos_ordenadas[1].landmark
        
        dedos_izq, *_ = evaluar_mano(m_izq)
        dedos_der, *_ = evaluar_mano(m_der)
        
        # Calculamos el vector de inclinación (desde la muñeca [0] hasta el nudillo medio [9])
        dx_izq = m_izq[9].x - m_izq[0].x
        dy_izq = m_izq[9].y - m_izq[0].y
        
        dx_der = m_der[9].x - m_der[0].x
        dy_der = m_der[9].y - m_der[0].y

        # Para el gesto del monito, las manos deben estar abiertas Y con inclinación "diagonal" interna:
        ancho_palma_izq = abs(dy_izq)
        ancho_palma_der = abs(dy_der)
        
        inclinadas_hacia_adentro = (dx_izq > ancho_palma_izq * 0.18) and (dx_der < -ancho_palma_der * 0.18)
        
        if dedos_izq >= 4 and dedos_der >= 4 and inclinadas_hacia_adentro:
            return 'mono sorpresa'
        
    #--------------------------------------------------------------
    # GESTOS CON UNA SOLA MANO
    #--------------------------------------------------------------
    puntos_primera_mano = resultados.multi_hand_landmarks[0].landmark
    total, indice, medio, anular, menique, pulgar = evaluar_mano(puntos_primera_mano)

    # Clasificación por descarte de condiciones
    if indice and not any([medio, anular, menique, pulgar]): 
        return 'mono idea'
    if pulgar and indice and not any([medio, anular, menique]): 
        return 'mono pensando'
    if total >= 4: 
        return 'mono hola'
    if total <= 1: 
        return 'mono cerrado'

    return 'ninguno'

# Loop de Ejecución y Renderizado -------------------------------------------------------

def main():
    imagenes = cargar_imagenes()
    cap = cv2.VideoCapture(0)
    print("Corriendo. Presiona ESC para salir.")

    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break

        frame = cv2.flip(frame, 1)                      # Espejo horizontal para comodidad del usuario
        rgb   = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)   # Conversión obligatoria para MediaPipe
        res   = detector.process(rgb)                   # Procesamiento de los frames mediante la IA

        gesto = 'ninguno'
        if res.multi_hand_landmarks:
            gesto = analizar_gestos(res)
            # Dibujamos las conexiones y puntos sobre la marcha
            for hand_lm in res.multi_hand_landmarks:
                mp_draw.draw_landmarks(frame, hand_lm, mp_hands.HAND_CONNECTIONS)

        # ventana dividida (Cámara + Imagen del gesto detectado)
        cam_ui   = cv2.resize(frame, (480, 360))
        img_ui   = cv2.resize(imagenes.get(gesto, crear_placeholder('ninguno')), (300, 360))
        combined = np.hstack((cam_ui, img_ui))

        # Etiqueta del estado actual del gesto en pantalla
        etiqueta = "HOLA" if gesto == 'mono hola' else gesto.upper()
        cv2.putText(combined, f"GESTO: {etiqueta}", (20, 40), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 0), 2)

        cv2.imshow('Proyecto monitos IA', combined)
        
        # Captura de teclado para cierre seguro con la tecla Escape
        if cv2.waitKey(1) & 0xFF == 27:
            break

    # Apagado y liberación segura de la webcam y ventanas de memoria
    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()