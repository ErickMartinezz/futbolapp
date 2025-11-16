⚽ Análisis técnico de imagen futbolística
Esta app en Python con Streamlit permite analizar imágenes de fútbol de forma técnica y visual.
Detecta la pelota, jugadores, clasifica equipos por color, calcula distancias y resalta líneas del campo.
Incluye marcación manual interactiva para mayor precisión.

📦 Estructura del proyecto
- main.py: interfaz principal de la app
- ubicar_pelota_y_jugadores.py: detecta pelota y jugadores, calcula distancias
- clasificar_bn.py: clasifica jugadores como "Claro" u "Oscuro" según intensidad
- analisis_avanzado.py: detecta líneas del campo con OpenCV
- estilo_futbol.py: aplica temas visuales (césped, estadio, nocturno, clásico)
- data/: carpeta donde van las imágenes
- 
🚀 Cómo usar la app
- Ejecutar con Streamlit:
streamlit run main.py
- En la interfaz:
- Elegís un tema visual
- Cargás una imagen desde la carpeta data o subís una nueva
- Ajustás el umbral para clasificar equipos
- Activás el checkbox para marcar la pelota manualmente si lo necesitás
- Marcás la pelota con el mouse sobre el canvas
- Automáticamente se detectan jugadores y se calculan distancias

✅ Requisitos
- Python 3.8 o superior
- Librerías necesarias: ver requirements.txt

🧠 Notas
- Todo corre en CPU, sin modelos pesados ni dependencias externas
- Ideal para presentaciones académicas o análisis táctico básico
- El código está modularizado para facilitar futuras mejoras
- La marcación manual permite corregir detecciones en imágenes complejas
