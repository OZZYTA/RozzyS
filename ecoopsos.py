# Import required libraries
import pymysql
import pandas as pd
import streamlit as st
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
import matplotlib.pyplot as plt
from plotly.subplots import make_subplots
import datetime
import webbrowser


# @st.cache(suppress_st_warning=True)
# @st.cache(allow_output_mutation=True)

def app():
    st.header('SEGUIMIENTO DE PQR - ECOOPSOS')
#     st.subheader("Listado de PQR")
    connection = pymysql.connect(host='107.180.43.4',
                                user='medico_web',
                                password='Medicontrol123*',
                                db='medico_rozzys',
                                cursorclass=pymysql.cursors.DictCursor)
    cursor = connection.cursor()
    sql = "SELECT * FROM pqr"
    df = pd.read_sql(sql, connection)
    cursor.execute(sql)
    result = cursor.fetchone()
    connection.close()
    
    df["motivo"][df['descripcion'].str.contains("medicamento")] = "MEDICAMENTOS"
    df["motivo"][df['descripcion'].str.contains("medicamentos")] = "MEDICAMENTOS"
    df["motivo"][df['descripcion'].str.contains("pastilla")] = "MEDICAMENTOS"
    df["motivo"][df['descripcion'].str.contains("pastillas")] = "MEDICAMENTOS"
    df["motivo"][df['descripcion'].str.contains("inyecciones")] = "MEDICAMENTOS"
    df["motivo"][df['descripcion'].str.contains("inyeccion")] = "MEDICAMENTOS"
    df["motivo"][df['descripcion'].str.contains("formula")] = "MEDICAMENTOS"
    df["motivo"][df['descripcion'].str.contains("pañales")] = "MEDICAMENTOS"
    df['fechainc'] =  pd.to_datetime(df['fechainc'], format='%Y-%m-%d')
    df['mes']=df['fechainc'].dt.strftime("%m")
    df['mes']=df['mes'].str.replace("01", "Enero")
    df['mes']=df['mes'].str.replace("02", "Febrero")
    df['mes']=df['mes'].str.replace("03", "Marzo")
    df['mes']=df['mes'].str.replace("04", "Abril")
    df['mes']=df['mes'].str.replace("05", "Mayo")
    df['mes']=df['mes'].str.replace("06", "Junio")
    df['mes']=df['mes'].str.replace("07", "Julio")
    df['mes']=df['mes'].str.replace("08", "Agosto")
    df['mes']=df['mes'].str.replace("09", "Septiembre")
    df['mes']=df['mes'].str.replace("10", "Octubre")
    df['mes']=df['mes'].str.replace("11", "Noviembre")
    df['mes']=df['mes'].str.replace("12", "Diciembre")
    df['eps']=df['eps'].str.replace('ECOOPSOS EPS','ECOOPSOS')
    dfecoopsos=df[(df['eps'] == "ECOOPSOS")]
    full=len(dfecoopsos)
    st.write("Al día de hoy, Medicontrol SAS ha recibido en total ",full," PQRs enviadas directamente por las EPS Ecoopsos, las mismas han sido solicitadas con el fin de hacer seguimiento y vigilancia al comportamiento resolutivo de cada uno de las Peticiones, Quejas o Reclamos de los usuarios por partes de la EAPB.")
    
    st.write("Por favor seleccione el rango de fechas que desea consultar:")
    today = datetime.date.today()
    tomorrow = today + datetime.timedelta(days=1)
    start_date = st.date_input('Fecha Inicial', datetime.date(2020,7,1))
    start_date=np.datetime64(start_date)
    end_date = st.date_input('Fecha Final', datetime.date(2020,12,1))
    end_date=np.datetime64(end_date) 
    
    dfecoopsos['fechainc'] = pd.to_datetime(dfecoopsos['fechainc'], format='%Y-%m-%d')
    mask = (dfecoopsos['fechainc'] > start_date) & (dfecoopsos['fechainc'] <= end_date)
    dfecoopsos = dfecoopsos.loc[mask]
    
    dfver=dfecoopsos[(dfecoopsos['fecha'] != "0000-00-00")]
    total=len(dfecoopsos)
    ver=len(dfver)
 
    st.write(" En el tiempo comprendido entre las fechas ",start_date," y ",end_date,", fueron recibidas ", total," PQR correspondientes a Ecoopsos EPS. De estas han sido verificadas ", ver," a través de medios sincrónicos no presenciales. Y a continuación se muestra la información analizada a partir de dicha verificación.")
    is_check = st.checkbox("Ver Tabla de PQR")
    if is_check:
        st.write(dfver)
        
    fig1 = px.histogram(dfver, x="mes")
    fig2 = px.histogram(dfver, x="motivo")
    fig3 = px.histogram(dfver, x="servicio")
    fig4 = px.histogram(dfver, x="estado")
    fig5 = px.histogram(dfver, x="indicador", width=150, height=300)
    
    col1, col2 = st.beta_columns(2)
    with col1:
        st.subheader("PQRs por Mes")
        st.write("Aqui puede observar el histograma de radicación de PQR de la EPS Ecoopsos durante el periodo seleccionado.")
        st.plotly_chart(fig1, use_container_width=True)
    with col2:
        st.subheader("Motivo de Radicación de las PQR")
        st.write("Informe gráfico con los diferentes motivos manifestados por los usuarios al momento de radicar su PQR en el periodo seleccionado.")
        st.plotly_chart(fig2, use_container_width=True)
    
    col3, col4 = st.beta_columns(2)
    with col3:
        st.subheader("Servicios implicados en las PQR")
        st.write("Areas y servicios por las cuales los usuarios establecieron sus PQR en el periodo seleccionado.")
        st.plotly_chart(fig3, use_container_width=True)
    with col4:
        st.subheader("Estado de las PQR")
        st.write("Al día de hoy, despues de realizada la verificación con los usuarios esta es la condición en la que se encuentran las PQR, radicadas en el periodo seleccionado.")
        st.plotly_chart(fig4, use_container_width=True)
        
    st.subheader("Estado actual por motivo")
    detalle=dfver.groupby([dfver.motivo, dfver.estado]).count().reset_index()
    detalle=detalle.sort_values('tipoid', ascending=False)
    x=detalle['motivo']
    y=detalle['tipoid']
    color=detalle['estado']
    fig6 = px.bar(detalle, x=x, y=y, color=color)
    st.plotly_chart(fig6, use_container_width=True)
        
    st.subheader("Indicador de satisfacción")
    st.write("Después de verificar con los usuarios y confirmar cuales de las PQR radicadas durante el periodo seleccionado se encontraban resueltas y cerradas, se consulto el estado de satisfacción del usuario con respecto a la resolución brindada por parte de la EAPB.")
    st.plotly_chart(fig5, use_container_width=True)
    
    st.write("Si desea consultar el detalle de cada PQR, por favor ingrese al aplicativo RozzyS con su nombre de usuario y contraseña.")
    url = 'http://medicontrolsas.com/RozzyS/'
    if st.button('Abrir RozzyS'):
        webbrowser.open_new_tab(url)
  
