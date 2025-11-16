import streamlit as st
import os
import cv2
import numpy as np
from PIL import Image
from streamlit_drawable_canvas import st_canvas

from ubicar_pelota_y_jugadores import ubicar_pelota_y_jugadores
from estilo_futbol import aplicar_estilo_tema
from analisis_avanzado import detectar_lineas_campo

# 📁 Configuración inicial
st.set_page_config(layout="wide")
st.title("⚽ Análisis técnico de imagen futbolística")

# 🎨 Selector de tema visual
tema = st.selectbox("Elegí un tema visual", ["Césped", "Estadio", "Nocturno", "Clásico"])
aplicar_estilo_tema(tema)

# 📂 Carga de imágenes
st.sidebar.header("📸 Selección de imagen")
carpeta = "data"
imagenes = [img for img in os.listdir(carpeta) if img.lower().endswith((".jpg", ".jpeg", ".png"))]
imagen_seleccionada = st.sidebar.selectbox("Elegí una imagen", imagenes)

# 📤 Subida de nueva imagen
imagen_subida = st.sidebar.file_uploader("Subí una imagen nueva", type=["jpg", "jpeg", "png"])
if imagen_subida:
    ruta_nueva = os.path.join(carpeta, imagen_subida.name)
    with open(ruta_nueva, "wb") as f:
        f.write(imagen_subida.getbuffer())
    st.sidebar.success("Imagen subida correctamente")
    imagenes = [img for img in os.listdir(carpeta) if img.lower().endswith((".jpg", ".jpeg", ".png"))]
    imagen_seleccionada = imagen_subida.name

# 🧹 Reiniciar canvas al cambiar de imagen
st.session_state["canvas"] = None

# 📍 Procesamiento principal
ruta = os.path.join(carpeta, imagen_seleccionada)
umbral_bn = st.slider("Umbral de clasificación (Claro/Oscuro)", 50, 200, 120)

# ✅ Checkbox para activar marcado manual
usar_manual = st.checkbox("Marcar pelota manualmente")

# 🎛️ Slider de sensibilidad solo si no se usa modo manual
if not usar_manual:
    param2 = st.slider("Sensibilidad de detección de pelota (param2)", 10, 60, 30)
else:
    param2 = 30  # valor por defecto, no se usa si hay pelota manual

centro_pelota_manual = None
if usar_manual:
    st.subheader("🖱️ Marcá la pelota sobre la imagen")

    imagen_cv = cv2.imread(ruta)
    if imagen_cv is None:
        st.error("No se pudo cargar la imagen.")
    else:
        imagen_rgb = cv2.cvtColor(imagen_cv, cv2.COLOR_BGR2RGB)

        alto_original, ancho_original = imagen_rgb.shape[:2]
        nuevo_ancho = 800
        nuevo_alto = int((nuevo_ancho / ancho_original) * alto_original)
        imagen_redimensionada = cv2.resize(imagen_rgb, (nuevo_ancho, nuevo_alto))

        try:
            imagen_pil = Image.fromarray(imagen_redimensionada.astype("uint8"))
        except Exception as e:
            st.error(f"No se pudo convertir la imagen a formato PIL: {e}")
            imagen_pil = None

        if imagen_pil:
            canvas_result = st_canvas(
                fill_color="rgba(255, 0, 0, 0.3)",
                stroke_width=5,
                stroke_color="#ff0000",
                background_image=imagen_pil,
                update_streamlit=True,
                height=nuevo_alto,
                width=nuevo_ancho,
                drawing_mode="point",
                point_display_radius=5,
                key=f"canvas_{imagen_seleccionada}",
            )

            if canvas_result.json_data and canvas_result.json_data["objects"]:
                punto = canvas_result.json_data["objects"][0]
                cx = int(punto["left"] * ancho_original / nuevo_ancho)
                cy = int(punto["top"] * alto_original / nuevo_alto)
                centro_pelota_manual = (cx, cy)
                st.success(f"Pelota marcada en: ({cx}, {cy})")

# 🔄 Ejecutar detección con o sin pelota manual
imagen_procesada, mensaje, tabla = ubicar_pelota_y_jugadores(
    ruta, umbral_bn=umbral_bn, param2=param2, centro_pelota_manual=centro_pelota_manual
)

# 📷 Mostrar imagen procesada
st.image(imagen_procesada, caption="Imagen procesada", channels="BGR", width=800)

# 📊 Mostrar tabla técnica
st.subheader("📊 Tabla técnica")
st.markdown(f"**{mensaje}**")
st.dataframe(tabla, use_container_width=True)

# 📐 Detección de líneas del campo
st.subheader("📐 Detección de líneas del campo (OpenCV)")
if st.button("Detectar líneas del campo"):
    with st.spinner("Procesando líneas con OpenCV..."):
        imagen_lineas = detectar_lineas_campo(ruta)
        st.image(imagen_lineas, caption="Líneas detectadas", channels="BGR", width=800)
