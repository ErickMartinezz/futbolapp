import streamlit as st


def aplicar_estilo_tema(tema):
    """
    Aplica un estilo visual personalizado según el tema elegido.

    Parámetros:
    - tema: nombre del tema ('Césped', 'Estadio', 'Nocturno', 'Clásico')

    Efecto:
    - Modifica el fondo y el estilo de la app Streamlit
    """
    if tema == "Césped":
        fondo = "#0b6623"
        imagen = ""
    elif tema == "Estadio":
        fondo = "#1a1a1a"
        imagen = "https://upload.wikimedia.org/wikipedia/commons/6/6e/Soccer_field_-_empty.svg"
    elif tema == "Nocturno":
        fondo = "#000000"
        imagen = "https://upload.wikimedia.org/wikipedia/commons/3/3e/Night_stadium.jpg"
    else:  # Clásico o cualquier otro
        fondo = "#ffffff"
        imagen = ""

    # Inyectar estilo CSS en la app
    st.markdown(f"""
        <style>
        .stApp {{
            background-color: {fondo};
            background-image: url('{imagen}');
            background-size: cover;
            background-repeat: no-repeat;
            background-position: center;
        }}
        h1, h2, h3 {{
            color: #ffffff;
            text-shadow: 1px 1px 2px #000;
        }}
        .css-1v3fvcr, .css-1d391kg {{
            background-color: rgba(255, 255, 255, 0.1);
            border-radius: 10px;
        }}
        </style>
    """, unsafe_allow_html=True)