import cv2
import numpy as np

def clasificar_equipo_bn(imagen, x, y, w, h, umbral=100):
    """
    Clasifica un jugador como 'Claro' u 'Oscuro' según la intensidad media en escala de grises.

    Parámetros:
    - imagen: imagen original en formato BGR
    - x, y, w, h: coordenadas del bounding box del jugador
    - umbral: valor de corte para decidir si es claro u oscuro (default: 100)

    Retorna:
    - 'Claro' si la intensidad media es mayor al umbral
    - 'Oscuro' si es menor o igual
    """
    # Recortar la región del jugador
    recorte = imagen[y:y + h, x:x + w]

    # Convertir a escala de grises
    gris = cv2.cvtColor(recorte, cv2.COLOR_BGR2GRAY)

    # Calcular intensidad media
    intensidad_media = np.mean(gris)

    # Clasificar según el umbral
    return "Claro" if intensidad_media > umbral else "Oscuro"