import cv2
import numpy as np
import pandas as pd
from clasificar_bn import clasificar_equipo_bn

def ubicar_pelota_y_jugadores(ruta_imagen, umbral_bn=100, param2=30, centro_pelota_manual=None):
    """
    Detecta la pelota y jugadores en una imagen de fútbol.
    Si se marca manualmente, usa esa posición directamente.
    Clasifica jugadores por intensidad (Claro/Oscuro) y calcula distancias a la pelota.
    Devuelve la imagen procesada, un mensaje resumen y una tabla con los 3 jugadores más cercanos.
    """
    imagen = cv2.imread(ruta_imagen)
    if imagen is None:
        raise FileNotFoundError("No se pudo cargar la imagen.")

    salida = imagen.copy()
    jugadores = []
    centro_pelota = None

    # 1. Si se marcó manualmente, usar esa posición directamente
    if centro_pelota_manual:
        centro_pelota = centro_pelota_manual
        cv2.circle(salida, centro_pelota, 10, (0, 0, 255), 2)
        cv2.putText(salida, "Pelota (manual)", (centro_pelota[0]-10, centro_pelota[1]-10),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 1)
    else:
        # 2. Detección automática con HoughCircles
        gris = cv2.cvtColor(imagen, cv2.COLOR_BGR2GRAY)
        gris = cv2.GaussianBlur(gris, (9, 9), 2)
        gris = cv2.equalizeHist(gris)

        circulos = cv2.HoughCircles(gris, cv2.HOUGH_GRADIENT, dp=1.2, minDist=30,
                                     param1=50, param2=param2, minRadius=5, maxRadius=30)

        if circulos is not None:
            circulos = np.uint16(np.around(circulos))
            for i in circulos[0, :1]:  # solo el más claro
                centro_pelota = (i[0], i[1])
                cv2.circle(salida, centro_pelota, i[2], (0, 0, 255), 2)
                cv2.putText(salida, "Pelota", (i[0]-10, i[1]-10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 1)

    # 3. Eliminar fondo verde del campo
    hsv = cv2.cvtColor(imagen, cv2.COLOR_BGR2HSV)
    mascara_campo = cv2.inRange(hsv, np.array([35, 40, 40]), np.array([85, 255, 255]))
    sin_campo = cv2.bitwise_not(mascara_campo)

    # 4. Detectar jugadores por contornos verticales
    contornos, _ = cv2.findContours(sin_campo, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    for c in contornos:
        x, y, w, h = cv2.boundingRect(c)
        if h > 40 and w/h < 1.5:
            centro = (x + w//2, y + h//2)
            equipo = clasificar_equipo_bn(imagen, x, y, w, h, umbral=umbral_bn)
            jugadores.append((centro, equipo))
            cv2.rectangle(salida, (x, y), (x + w, y + h), (0, 255, 0), 2)
            cv2.putText(salida, equipo, (x, y - 5), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1)

    # 5. Calcular distancias a la pelota
    distancias = []
    if centro_pelota:
        distancias = [(jugador, np.linalg.norm(np.array(jugador[0]) - np.array(centro_pelota))) for jugador in jugadores]
        distancias = sorted(distancias, key=lambda x: x[1])[:3]

        for (centro, equipo), dist in distancias:
            cv2.line(salida, centro_pelota, centro, (255, 0, 0), 2)
            cv2.putText(salida, f"{equipo} a {int(dist)}px", centro, cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1)

    # 6. Armar mensaje y tabla
    if centro_pelota and distancias:
        mensaje = f"Pelota ubicada. Jugadores más cercanos: {len(distancias)}"
        datos = [{
            "Equipo": equipo,
            "Distancia (px)": int(dist),
            "Posición": f"{centro[0]}, {centro[1]}"
        } for (centro, equipo), dist in distancias]
        tabla = pd.DataFrame(datos)
    else:
        mensaje = "No se detectó la pelota."
        tabla = pd.DataFrame(columns=["Equipo", "Distancia (px)", "Posición"])

    return salida, mensaje, tabla