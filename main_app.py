import app1
import coomeva
import comfaoriente
import comparta
import compensar
import coosalud
import medimas
import ecoopsos
import nuevaeps
import sanitas
import streamlit as st
from PIL import Image

# Set the sidebar color
st.markdown(
    """
<style>
.sidebar .sidebar-content {
    background-image: linear-gradient(#435B97, #537FBC);
    color: white;
}
</style>
""",
    unsafe_allow_html=True,
)

# Set the sidebar image
image = Image.open("./MC_logo.png")
st.sidebar.image(image, use_column_width=True)

# Set the sidebar title
st.sidebar.title('RozzyS Dashboard')

# Set the sidebar selectbox for choosing dashboard
PAGES = {
    "Informe Global": app1,
    "Comfaoriente EPS": comfaoriente,
    "Comparta": comparta,
    "Compensar": compensar,
    "Coomeva EPS": coomeva,
    "Coosalud": coosalud,
    "Ecoopsos": ecoopsos,
    "Medimas EPS": medimas,
    "Nueva EPS": nuevaeps,
    "Sanitas": sanitas
}
st.sidebar.write("Vea aqui el informe gráfico respecto al estado e información de las PQR radicadas para cada una de las EPS tanto en sus buzones como en los buzones del SAC de la secretaria de Salud del Municipio de Cúcuta.")
st.sidebar.subheader("Seleccione la EPS")
selection = st.sidebar.selectbox("", list(PAGES.keys()))
page = PAGES[selection]
page.app()

# Set author names on the sidebar using markdown
st.sidebar.markdown(

    """<h6><br><br><br><br><br><strong><b>Developed by:</strong><br>
<strong><br><b>Ozzyta - Medicontrol SAS<br />
  <b><br /></b></strong></h6>


""", unsafe_allow_html=True)
