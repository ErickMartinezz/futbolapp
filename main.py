if usar_manual:
    st.subheader("🖱️ Marcá la pelota sobre la imagen")

    imagen_cv = cv2.imread(ruta)
    if imagen_cv is None:
        st.error("No se pudo cargar la imagen.")
    else:
        imagen_rgb = cv2.cvtColor(imagen_cv, cv2.COLOR_BGR2RGB)

        # ✅ Redimensionar a 800 px de ancho manteniendo proporción
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
