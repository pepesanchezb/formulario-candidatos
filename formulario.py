# -*- coding: utf-8 -*-
"""
Formulario profesional de selección de candidatos
Puesto: Técnico Junior de Automatización con Python
Autor: Monomyc (2025‑06‑11)
"""

import streamlit as st
import pandas as pd
from datetime import datetime
from pathlib import Path

###############################################################################
# CONFIGURACIÓN BÁSICA DE LA PÁGINA
###############################################################################
st.set_page_config(
    page_title="Selección de Candidatos · Automatización Python",
    page_icon="🛠️",                 # Emoji como favicon
    layout="centered",               # Diseño centrado para mejor legibilidad
)

###############################################################################
# ESTILOS RESPONSIVOS (MÓVIL ↔ DESKTOP)
###############################################################################
st.markdown(
    """
    <style>
        /* Contenedor principal */
        .main .block-container {
            padding-top: 2rem;
            max-width: 820px;      /* Máx. ancho en desktop */
            margin: 0 auto;       /* Centrado */
        }

        /* Columnas responsivas: en móvil se apilan */
        @media (max-width: 600px) {
            div[data-testid="column"] {
                width: 100% !important;  /* Una columna ocupa todo el ancho */
                flex-direction: column !important;
            }
        }
    </style>
    """,
    unsafe_allow_html=True,
)

###############################################################################
# ENCABEZADO
###############################################################################
# División en 3 columnas para alinear logo, título y espacio vacío
col_logo, col_title, _ = st.columns([1, 6, 1])

with col_logo:
    # Logo de empresa (sustituir 'logo.png' por la ruta real)
    st.image("https://via.placeholder.com/80x80.png?text=LOGO", width=80)

with col_title:
    st.markdown("## 🛠️ Selección de Técnico Junior de Automatización con Python")
    st.markdown(
        "Como ves en este formulario, claramente necesitamos un programador que nos ayude a mejorarlo 😅"
    )

st.markdown("---")

###############################################################################
# FORMULARIO
###############################################################################
with st.form(key="form_candidato"):
    # Distribución en columnas para organizar los campos
    c1, c2 = st.columns(2)

    with c1:
        nombre = st.text_input("**Nombre completo** ✍️", max_chars=100)
        email = st.text_input("**Email de contacto** 📧", max_chars=100)
        github = st.text_input("**Enlace a portfolio o GitHub** 🔗")

    with c2:
        nivel_python = st.radio(
            "**Nivel de Python** 🐍",
            options=["Básico", "Medio", "Avanzado"],
            horizontal=False,
        )

        st.markdown("**APIs que conoces** 🌐")
        api_google, api_shopify, api_holded, api_otra = st.columns(4)
        with api_google:
            api_google_val = st.checkbox("Google Sheets")
        with api_shopify:
            api_shopify_val = st.checkbox("Shopify")
        with api_holded:
            api_holded_val = st.checkbox("Holded")
        with api_otra:
            api_otra_val = st.checkbox("Otra")

        otra_api_text = ""
        if api_otra_val:
            otra_api_text = st.text_input("¿Cuál otra API? 📝", max_chars=100)

    # Separador visual
    st.markdown("---")

    # Resto de campos (una sola columna para mayor anchura)
    experiencia_back = st.text_area(
        "**Experiencia con Streamlit, Flask o Dash** 🗒️",
        height=120,
    )
    librerias_viz = st.text_area(
        "**Librerías de visualización que has usado** 📊",
        height=120,
    )
    ejemplo_proyecto = st.text_input(
        "**Enlace a ejemplo práctico o proyecto** 🔬",
    )

    c3, c4 = st.columns(2)
    with c3:
        disponibilidad = st.text_input("**Disponibilidad horaria semanal** ⏱️")
    with c4:
        pretension = st.text_input("**Pretensión económica (€)** 💶")

    comentario = st.text_area("**Comentario adicional o motivación** 💡", height=120)

    # Botón de envío
    enviar = st.form_submit_button(label="📨 Enviar candidatura")

###############################################################################
# VALIDACIÓN Y ALMACENAMIENTO
###############################################################################
if enviar:
    errores = []

    # Validación básica
    if not nombre.strip():
        errores.append("• El nombre completo es obligatorio.")
    if not email.strip():
        errores.append("• El email de contacto es obligatorio.")
    if not nivel_python:
        errores.append("• Debes elegir tu nivel de Python.")

    if errores:
        st.error("Por favor, corrige los siguientes errores:\n" + "\n".join(errores))
    else:
        # Construir registro como diccionario
        registro = {
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "nombre": nombre.strip(),
            "email": email.strip(),
            "portfolio_github": github.strip(),
            "nivel_python": nivel_python,
            "api_google_sheets": api_google_val,
            "api_shopify": api_shopify_val,
            "api_holded": api_holded_val,
            "api_otra": api_otra_val,
            "otra_api_nombre": otra_api_text.strip(),
            "experiencia_backend": experiencia_back.strip(),
            "librerias_visualizacion": librerias_viz.strip(),
            "ejemplo_proyecto": ejemplo_proyecto.strip(),
            "disponibilidad": disponibilidad.strip(),
            "pretension_eur": pretension.strip(),
            "comentario": comentario.strip(),
        }

        # Ruta al CSV en la misma carpeta del script
        csv_path = Path(__file__).parent / "respuestas_candidatos.csv"

        # Cargar CSV si existe, sino crear uno nuevo
        if csv_path.exists():
            df = pd.read_csv(csv_path)
            df = pd.concat([df, pd.DataFrame([registro])], ignore_index=True)
        else:
            df = pd.DataFrame([registro])

        # Guardar CSV
        df.to_csv(csv_path, index=False)

        # Confirmación al usuario
        st.success("✅ ¡Tu candidatura se ha enviado correctamente!")
        st.balloons()

###############################################################################
# BARRA LATERAL (OPCIONAL)
###############################################################################
