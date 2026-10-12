import streamlit as st
import pandas as pd
import folium
from streamlit_folium import st_folium
import bcrypt
from pathlib import Path

# =====================================================
# CONFIGURACION GENERAL
# =====================================================

st.set_page_config(
    page_title="CONSULTA ELECTORAL - REGIONAL 2026",
    layout="wide"
)

COLOR_PRINCIPAL = "#e30613"

# =====================================================
# LOGIN
# =====================================================

USUARIOS = {
    "admin": bcrypt.hashpw(
        "123456".encode(),
        bcrypt.gensalt()
    )
}

def login():

    st.image("logo_nacion.png", width=180)

    st.markdown(
        "<h1 style='color:red;'>CONSULTA ELECTORAL - REGIONAL 2026</h1>",
        unsafe_allow_html=True
    )

    usuario = st.text_input("Usuario")
    password = st.text_input(
        "Contraseña",
        type="password"
    )

    if st.button("Ingresar"):

        if usuario in USUARIOS:

            valido = bcrypt.checkpw(
                password.encode(),
                USUARIOS[usuario]
            )

            if valido:
                st.session_state.login = True
                st.rerun()

        st.error("Credenciales inválidas")

# =====================================================
# CARGA EXCEL
# =====================================================

@st.cache_data
def cargar_padron():

    archivo = "Maestro_EMR2026.xlsx"

    if Path(archivo).exists():

        df = pd.read_excel(
            archivo,
            engine="openpyxl"
        )

        return df

    return pd.DataFrame()

# =====================================================
# DASHBOARD
# =====================================================

def dashboard(df):

    st.header("Dashboard Electoral")

    total_mesas = len(df)

    c1,c2,c3,c4 = st.columns(4)

    c1.metric(
        "Mesas",
        total_mesas
    )

    c2.metric(
        "Locales",
        df["LOCAL_VOTACION"].nunique()
        if "LOCAL_VOTACION" in df.columns
        else 0
    )

    c3.metric(
        "Distritos",
        df["DISTRITO"].nunique()
        if "DISTRITO" in df.columns
        else 0
    )

    c4.metric(
        "Provincias",
        df["PROVINCIA"].nunique()
        if "PROVINCIA" in df.columns
        else 0
    )

# =====================================================
# CONSULTAS
# =====================================================

def consultas(df):

    st.header(
        "Consulta de Mesas de Votación"
    )

    provincia = ""
    distrito = ""
    localidad = ""

    if "PROVINCIA" in df.columns:

        provincia = st.selectbox(
            "Provincia",
            ["TODOS"] +
            sorted(df["PROVINCIA"].dropna().unique())
        )

    datos = df.copy()

    if provincia != "TODOS":
        datos = datos[
            datos["PROVINCIA"] == provincia
        ]

    if "DISTRITO" in datos.columns:

        opciones = (
            ["TODOS"]
            +
            sorted(datos["DISTRITO"].dropna().unique())
        )

        distrito = st.selectbox(
            "Distrito",
            opciones
        )

    if distrito != "TODOS":
        datos = datos[
            datos["DISTRITO"] == distrito
        ]

    if "LOCALIDAD" in datos.columns:

        opciones = (
            ["TODOS"]
            +
            sorted(datos["LOCALIDAD"].dropna().unique())
        )

        localidad = st.selectbox(
            "Localidad",
            opciones
        )

    if localidad != "TODOS":
        datos = datos[
            datos["LOCALIDAD"] == localidad
        ]

    st.dataframe(
        datos,
        use_container_width=True
    )

# =====================================================
# PERSONEROS
# =====================================================

def personeros():

    st.header("Control de Personeros")

    dni = st.text_input("DNI")

    nombre = st.text_input(
        "Nombre Completo"
    )

    mesa = st.text_input(
        "Mesa Asignada"
    )

    telefono = st.text_input(
        "Teléfono"
    )

    estado = st.selectbox(
        "Estado",
        [
            "Confirmado",
            "Pendiente",
            "Sin Cobertura"
        ]
    )

    if st.button("Registrar Personero"):

        st.success(
            f"Personero {nombre} registrado"
        )

# =====================================================
# INCIDENCIAS
# =====================================================

def incidencias():

    st.header(
        "Registro de Incidencias"
    )

    mesa = st.text_input(
        "Mesa"
    )

    tipo = st.selectbox(
        "Tipo",
        [
            "Ausencia Personero",
            "Impugnación",
            "Observación",
            "Material Electoral",
            "Otro"
        ]
    )

    descripcion = st.text_area(
        "Descripción"
    )

    foto = st.file_uploader(
        "Fotografía"
    )

    if st.button(
        "Guardar Incidencia"
    ):

        st.success(
            "Incidencia registrada"
        )

# =====================================================
# RESULTADOS
# =====================================================

def resultados():

    st.header(
        "Carga de Resultados"
    )

    mesa = st.text_input(
        "Mesa de Votación"
    )

    ahora_nacion = st.number_input(
        "Ahora Nación",
        min_value=0
    )

    rival = st.number_input(
        "Oponente",
        min_value=0
    )

    blancos = st.number_input(
        "Blancos",
        min_value=0
    )

    nulos = st.number_input(
        "Nulos",
        min_value=0
    )

    observados = st.number_input(
        "Observados",
        min_value=0
    )

    acta = st.file_uploader(
        "Foto del Acta"
    )

    if st.button(
        "Guardar Resultado"
    ):

        st.success(
            "Resultado registrado"
        )

# =====================================================
# MAPA ELECTORAL
# =====================================================

def mapa_electoral():

    st.header(
        "Mapa Electoral"
    )

    mapa = folium.Map(
        location=[
            -18.0146,
            -70.2536
        ],
        zoom_start=10
    )

    folium.Marker(
        [
            -18.0146,
            -70.2536
        ],
        popup="Tacna"
    ).add_to(mapa)

    st_folium(
        mapa,
        width=1200,
        height=600
    )

# =====================================================
# SEMAFORO
# =====================================================

def inteligencia():

    st.header(
        "Inteligencia Electoral"
    )

    cobertura = st.slider(
        "Cobertura de Personeros %",
        0,
        100,
        85
    )

    if cobertura >= 90:

        st.success(
            "🟢 FORTALEZA"
        )

    elif cobertura >= 70:

        st.warning(
            "🟡 EN DISPUTA"
        )

    else:

        st.error(
            "🔴 RIESGO"
        )

# =====================================================
# APP 
