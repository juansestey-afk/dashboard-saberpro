import pandas as pd
import streamlit as st
import plotly.express as px


# Leer Excel
df = pd.read_excel("Consolidado 2017-2026-1.xlsx")
df = df.rename(columns={
    "COMUNCACIÓN ESCRITA": "COMUNICACIÓN ESCRITA"
})

# Título
st.title("Dashboard Saber Pro")

st.markdown("""
<style>
[data-testid="stMetricValue"] {
    font-size: 18px;
}
</style>
""", unsafe_allow_html=True)

# Lista de años
anios = ["Todos"] + sorted(df["Periodo"].unique().tolist())

# Filtro
anio_seleccionado = st.selectbox(
    "Seleccione un año",
    anios
)

# Aplicar filtro
if anio_seleccionado == "Todos":
    df_filtrado = df
else:
    df_filtrado = df[df["Periodo"] == anio_seleccionado]

# Calcular promedio
promedio = df_filtrado["PUNTAJE GLOBAL"].mean()


# Total de estudiantes evaluados
total_estudiantes = len(df_filtrado)

# Competencias
competencias = [
    "COMUNICACIÓN ESCRITA",
    "RAZONAMIENTO CUANTITATIVO",
    "LECTURA CRÍTICA",
    "COMPETENCIAS CIUDADANAS",
    "INGLÉS"
]

# Promedio de cada competencia
promedios_comp = df_filtrado[competencias].mean()

# Mejor y peor competencia
mejor_competencia = promedios_comp.idxmax()
peor_competencia = promedios_comp.idxmin()

# Crear dos columnas
col1, col2, col3, col4 = st.columns(4)

# KPI 1
with col1:
    st.metric(
        label="Promedio Puntaje Global",
        value=round(promedio, 2)
    )

# KPI 2
with col2:
    st.metric(
        label="Estudiantes Evaluados",
        value=total_estudiantes
    )
    
# KPI 3   
with col3:
    st.metric(
        label="Mejor Competencia",
        value=mejor_competencia
    )
# KPI 3 
with col4:
    st.metric(
        label="Peor Competencia",
        value=peor_competencia
    )
    
    
# Tendencia del puntaje global

tendencia = (
    df.groupby("Periodo")["PUNTAJE GLOBAL"]
    .mean()
    .reset_index()
)

fig_tendencia = px.line(
    tendencia,
    x="Periodo",
    y="PUNTAJE GLOBAL",
    title="Tendencia del Puntaje Global",
    markers=True
)



fig_tendencia.update_layout(
    title_x=0.4,
    plot_bgcolor="white",
    paper_bgcolor="white",
    xaxis_title="Año",
    yaxis_title="Promedio Puntaje Global"
)

fig_tendencia.update_traces(
    line=dict(
        color="#0ECC17",
        width=4
    )
)

st.plotly_chart(
    fig_tendencia,
    use_container_width=True
)



competencias = [
    "COMUNICACIÓN ESCRITA",
    "RAZONAMIENTO CUANTITATIVO",
    "LECTURA CRÍTICA",
    "COMPETENCIAS CIUDADANAS",
    "INGLÉS"
]

if anio_seleccionado == "Todos":

    datos_grafico = (
        df.groupby("Periodo")[competencias]
        .mean()
        .reset_index()
    )

else:

    datos_grafico = (
        df_filtrado[competencias]
        .mean()
        .reset_index()
    )

    datos_grafico.columns = [
        "Competencia",
        "Promedio"
    ]
    
# Gráfico cuando está seleccionado "Todos"
if anio_seleccionado == "Todos":

    datos_largos = datos_grafico.melt(
        id_vars="Periodo",
        var_name="Competencia",
        value_name="Promedio"
    )

    fig = px.bar(
        datos_largos,
        x="Periodo",
        y="Promedio",
        color="Competencia",
        barmode="group",
        title="Promedio de Competencias por Año",
         color_discrete_map={
                "COMUNICACIÓN ESCRITA": "#0CCF15",
                "RAZONAMIENTO CUANTITATIVO": "#17812E",
                "LECTURA CRÍTICA": "#234D08",
                "COMPETENCIAS CIUDADANAS": "#3DDB57",
                "INGLÉS": "#7BA775"
            }
    )

# Gráfico cuando se selecciona un año específico
else:

    fig = px.bar(
    datos_grafico,
    x="Competencia",
    y="Promedio",
    color="Competencia",
    title=f"Promedio de Competencias - {anio_seleccionado}",
    color_discrete_map={
        "COMUNICACIÓN ESCRITA": "#0CCF15",
        "RAZONAMIENTO CUANTITATIVO": "#17812E",
        "LECTURA CRÍTICA": "#234D08",
        "COMPETENCIAS CIUDADANAS": "#3DDB57",
        "INGLÉS": "#7BA775"
    }
)

fig.update_traces(
    texttemplate='%{y:.0f}',
    textposition='outside'
)
# Mostrar gráfico
st.plotly_chart(fig, use_container_width=True)
