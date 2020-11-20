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
    st.header('ESTADO GENERAL DE LAS PQR')
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
    full=len(df)
    df['eps']=df['eps'].str.replace('COMFAORIENTE EPS','COMFAORIENTE')
    df['eps']=df['eps'].str.replace('MEDIMAS EPS','MEDIMAS')
    st.write("Al día de hoy, Medicontrol SAS ha recibido en total ",full," PQRs enviadas directamente por las EPS, las mismas han sido solicitadas con el fin de hacer seguimiento y vigilancia al comportamiento resolutivo de cada uno de las Peticiones, Quejas o Reclamos de los usuarios por partes de las EAPB.")
    df_data=df.copy()
    st.write("Por favor seleccione el rango de fechas que desea consultar:")
    today = datetime.date.today()
    tomorrow = today + datetime.timedelta(days=1)
    start_date1 = st.date_input('Fecha Inicial', datetime.date(2020,7,1))
    start_date1=np.datetime64(start_date1)
    end_date1 = st.date_input('Fecha Final', datetime.date(2020,12,1))
    end_date1=np.datetime64(end_date1) 
    
    df_data['fechainc'] = pd.to_datetime(df_data['fechainc'], format='%Y-%m-%d')
    mask = (df_data['fechainc'] > start_date1) & (df_data['fechainc'] <= end_date1)
    df_data = df_data.loc[mask]
    
    dfver=df_data[(df_data['fecha'] != "0000-00-00")]
    total=len(df_data)
    ver=len(dfver)
 
    st.write(" En el tiempo comprendido entre las fechas ",start_date1," y ",end_date1,", fueron recibidas ", total," PQR en total. De estas han sido verificadas ", ver," a través de medios sincrónicos no presenciales. Y a continuación se muestra la información analizada a partir de dicha verificación.")
    is_check = st.checkbox("Ver Tabla de PQR")
    if is_check:
        st.write(dfver)
    
    #GLOBAL
    
    dfmes=dfver.groupby([dfver.mes]).count().reset_index()
    dfmes=dfmes.sort_values('tipoid', ascending=False)        
    dfeps=dfver.groupby([dfver.eps]).count().reset_index()
    dfeps=dfeps.sort_values('tipoid', ascending=False)
    dfmotivo=dfver.groupby([dfver.motivo]).count().reset_index()
    dfmotivo=dfmotivo.sort_values('tipoid', ascending=False)
    dfestado=dfver.groupby([dfver.estado]).count().reset_index()
    dfestado=dfestado.sort_values('tipoid', ascending=False)
    Xmes=dfmes['mes']
    Ymes=dfmes.tipoid
    Xeps=dfeps.eps
    Yeps=dfeps.tipoid
    Xmotivo=dfmotivo.motivo
    Ymotivo=dfmotivo.tipoid
    Xestado=dfestado.estado
    Yestado=dfestado.tipoid
    fig = make_subplots(
    rows=2, cols=2,
    specs=[[{"type": "xy"}, {"type": "domain"}],[{"type": "domain"}, {"type": "xy"}]],
    subplot_titles=("PQR x Mes", "PQR x EPS", "PQR x Motivo","PQR x Estado Actual"))
    fig.add_trace(go.Bar(x=Xmes, y=Ymes),
                  row=1, col=1)
    fig.add_trace(go.Pie(labels=Xeps, values=Yeps,showlegend=True),
                  row=1, col=2)
    fig.add_trace(go.Pie(labels=Xmotivo, values=Ymotivo),
                  row=2, col=1)
    fig.add_trace(go.Bar(x=Xestado, y=Yestado),
                  row=2, col=2)
    fig.update_layout(height=700, showlegend=False)
    fig.update_layout(title_text="Informe gráfico de las PQR radicadas en cada buzón de las EPS",font_size=10)
    st.plotly_chart(fig, use_container_width=True) 
    
    dfcerradas= dfver[(dfver['estado'] == 'RESUELTA')]
    cerradas=len(dfcerradas)
    st.subheader("Indicador de Satisfacción")
    st.write("Despues de llamar a los usuarios quejosos, se confirma que de las PQR verificadas ", cerradas, " se encuentran resueltas, a estos usuarios se les su percepción con respecto a la resolución que la EPS brindó a su PQR, el cual fue tomado como indicador (Satisfactorio o Insatisfactorio) y se representa a continuación.")
    
    dfindicador=dfcerradas.groupby([dfcerradas.indicador]).count().reset_index()
    dfindicador=dfindicador.sort_values('tipoid', ascending=False)
    Xindicador=dfindicador.indicador
    Yindicador=dfindicador.tipoid
    fig = go.Figure(data=[go.Pie(labels=Xindicador, values=Yindicador, hole=.4)])
    fig.update_layout(height=350, width=500,showlegend=True)
    st.plotly_chart(fig, use_container_width=True)

    #SAC
    st.header("SAC de la SSM de Cúcuta")
    st.write("Por favor seleccione el rango de fechas que desea consultar")
    
    today = datetime.date.today()
    tomorrow = today + datetime.timedelta(days=1)
    start_date = st.date_input('Fecha inicial', datetime.date(2020,7,1))
    start_date=np.datetime64(start_date)
    end_date = st.date_input('Fecha final', datetime.date(2020,12,1))
    end_date=np.datetime64(end_date)
    
    dfsac=df[(df['sac'] == "1")]
    dfsac['fechainc'] = pd.to_datetime(dfsac['fechainc'], format='%Y-%m-%d')
    mask = (dfsac['fechainc'] > start_date) & (dfsac['fechainc'] <= end_date)
    dfsac = dfsac.loc[mask]
    
    dfsacver=dfsac[(dfsac['fecha'] != "0000-00-00")]
    sac=len(dfsac)
    sacver=len(dfsacver)
    
    
    
    st.write("Entre las Fechas ", start_date, " y ", end_date," Se recibieron ",sac," PQR que fueron directamente enviadas y notificadas por el SAC de la Secretaria de Salud de Cúcuta, y de estas han sido verificadas y se encuentran en seguimiento ",sacver,". A continuación su informe gráfico:")
    
    topmes=dfsacver.groupby('mes').count().reset_index()
    topmes=topmes.sort_values('tipoid', ascending=False)
    topeps=dfsacver.groupby('eps').count().reset_index()
    topeps=topeps.sort_values('tipoid', ascending=False)   
    topmotivo=dfsacver.groupby('motivo').count().reset_index()
    topmotivo=topmotivo.sort_values('tipoid', ascending=False)
    topcondicion=dfsacver.groupby('estado').count().reset_index()
    topcondicion=topcondicion.sort_values('tipoid', ascending=False)
    xmes=topmes['mes']
    ymes=topmes.tipoid
    xeps=topeps.eps
    yeps=topeps.tipoid
    xmotivo=topmotivo.motivo
    ymotivo=topmotivo.tipoid
    xcondicion=topcondicion.estado
    ycondicion=topcondicion.tipoid
    fig = make_subplots(
    rows=1, cols=4,
    specs=[[{"type": "domain"}, {"type": "domain"},{"type": "domain"}, {"type": "domain"}]],
    subplot_titles=("PQR x Mes", "PQR x EPS", "PQR x Motivo","PQR x Estado Actual")
    )
    fig.add_trace(go.Pie(labels=xmes, values=ymes),
                  row=1, col=1)
    fig.add_trace(go.Pie(labels=xeps, values=yeps),
                  row=1, col=2)
    fig.add_trace(go.Pie(labels=xmotivo, values=ymotivo),
                  row=1, col=3)
    fig.add_trace(go.Pie(labels=xcondicion, values=ycondicion),
                  row=1, col=4)
    fig.update_layout(height=350, showlegend=False)
#     fig.update_layout(title_text="Informe gráfico de las PQR radicadas en el SAC de la SSM Cúcuta",font_size=10)
    st.plotly_chart(fig, use_container_width=True) 
    
    st.write("Si desea consultar el detalle de cada PQR, por favor ingrese al aplicativo RozzyS con su nombre de usuario y contraseña.")
    url = 'http://medicontrolsas.com/RozzyS/'
    if st.button('Abrir RozzyS'):
        webbrowser.open_new_tab(url)