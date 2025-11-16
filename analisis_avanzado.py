import cv2
import numpy as np


def detectar_lineas_campo(ruta_imagen):
    """
    Detecta líneas del campo de fútbol usando procesamiento de bordes y la transformada de Hough.

    Parámetros:
    - ruta_imagen: ruta local de la imagen a procesar

    Retorna:
    - imagen con las líneas detectadas dibujadas en verde
    """
    # Cargar imagen
    imagen = cv2.imread(ruta_imagen)
    if imagen is None:
        raise FileNotFoundError("No se pudo cargar la imagen.")

    # Convertir a escala de grises y suavizar
    gris = cv2.cvtColor(imagen, cv2.COLOR_BGR2GRAY)
    blur = cv2.GaussianBlur(gris, (5, 5), 0)

    # Detectar bordes con Canny
    edges = cv2.Canny(blur, 50, 150)

    # Detectar líneas con HoughLinesP
    lineas = cv2.HoughLinesP(edges, 1, np.pi / 180, threshold=100, minLineLength=80, maxLineGap=10)

    # Dibujar líneas sobre la imagen original
    salida = imagen.copy()
    if lineas is not None:
        for linea in lineas:
            x1, y1, x2, y2 = linea[0]
            cv2.line(salida, (x1, y1), (x2, y2), (0, 255, 0), 2)

    return salida