import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from streamlit_gsheets import GSheetsConnection

# ==========================================
# CONFIGURACIÓN DE LA PÁGINA Y ESTILOS UI
# ==========================================
st.set_page_config(
    page_title="Misión 3 - Dashboard Ejecutivo",
    page_icon="🏛️",
    layout="wide"
)

st.markdown("""
    <style>
    .main, [data-testid="stAppViewContainer"], [data-testid="stHeader"] { 
        background-color: #ffffff !important; 
    }
    div[data-testid="metric-container"] {
        background-color: #ffffff !important;
        border-top: 4px solid #0f172a !important;
        border-left: 1px solid #cbd5e1 !important;
        border-right: 1px solid #cbd5e1 !important;
        border-bottom: 1px solid #cbd5e1 !important;
        padding: 20px !important;
        border-radius: 8px !important;
        box-shadow: 0 4px 10px rgba(0, 0, 0, 0.02) !important;
    }
    [data-testid="stMetricValue"] { font-size: 30px !important; color: #000000 !important; font-weight: 700 !important; }
    [data-testid="stMetricLabel"] { font-size: 14px !important; color: #334155 !important; font-weight: 600 !important; }
    h1 { color: #000000 !important; font-family: Arial, sans-serif; font-weight: 700; }
    h2, h3 { color: #0f172a !important; font-family: Arial, sans-serif; font-weight: 600; }
    p, span, li, td, th { color: #000000 !important; }
    </style>
    """, unsafe_allow_html=True)

# CONTROLES CRUCIALES DE MEMORIA EN BARRA LATERAL
st.sidebar.markdown("### 🛠️ Panel de Control Analítico")
if st.sidebar.button("🔄 Borrar Memoria Caché de la App"):
    st.cache_data.clear()
    st.sidebar.success("¡Caché destruida e inicializada!")

# ==========================================
# CONEXIÓN DIRECTA Y CONTROLADA A GOOGLE SHEETS
# ==========================================
url_directa = "https://docs.google.com/spreadsheets/d/1aEIyDmHuHxzei8IRqMFKYDIZ1Hc3lvQoU6odzyuiL9M/edit?usp=sharing"

@st.cache_data(ttl="1s") # Reducido a 1 segundo para forzar consultas calientes a la API
def cargar_pestana(nombre_pestana):
    conn = st.connection("gsheets", type=GSheetsConnection)
    return conn.read(spreadsheet=url_directa, sheet=nombre_pestana)

try:
    df_plataformas = cargar_pestana("Plataformas")
    df_gestion = cargar_pestana("Gestion_EI")
    df_eventos = cargar_pestana("Eventos_EULAC")
    
    # Limpieza rigurosa de metadatos de las columnas de strings
    for df_actual in [df_plataformas, df_gestion, df_eventos]:
        df_actual.columns = df_actual.columns.str.strip()
    
    df_gestion['Categoria'] = df_gestion['Categoria'].astype(str).str.strip().str.lower()
    df_gestion['Item_Limpio'] = df_gestion['Item'].astype(str).str.strip().str.lower()
    df_gestion['Valor_Num'] = pd.to_numeric(df_gestion['Valor'], errors='coerce')
except Exception as e:
    st.error(f"⚠️ Error crítico en la llamada de datos: {e}")
    st.stop()

# ==========================================
# DESPLIEGUE DE COMPONENTES DE INTERFAZ
# ==========================================
st.title("🏛️ Centro de Emprendimiento e Innovación - Misión 3")
st.markdown("### **Dashboard de Indicadores Estratégicos y de Gestión**")
st.markdown("---")

# KPIs de Plataformas
st.subheader("🏢 Estado de la Unidad y Plataformas")
cols_plat = st.columns(len(df_plataformas))
for index, row in df_plataformas.iterrows():
    with cols_plat[index % len(df_plataformas)]:
        st.metric(label=str(row['Plataforma']), value=str(row['Estado']))

st.markdown("---")

# Contenedores Gráficos de Gestión
col_izq, col_der = st.columns([1.2, 1])

with col_izq:
    st.subheader("🚀 Embudo del Emprendedor (E&I)")
    df_funnel_data = df_gestion[df_gestion['Categoria'] == 'programa'].copy()
    df_funnel_data['Item_Display'] = df_funnel_data['Item'].astype(str).str.capitalize()

    fig_embudo = go.Figure(go.Funnel(
        y=df_funnel_data['Item_Display'],
        x=df_funnel_data['Valor_Num'],
        textinfo="value",
        marker={"color": ["#0f172a", "#334155", "#64748b"]}
    ))
    fig_embudo.update_layout(template="plotly_white", height=350, plot_bgcolor='#ffffff', paper_bgcolor='#ffffff', font=dict(color="#000000"))
    st.plotly_chart(fig_embudo, use_container_width=True)

with col_der:
    st.subheader("🌐 Comunidad Digital (Redes Sociales)")
    
    # SEPARACIÓN Y FILTRADO ESTÁNDAR
    df_redes = df_gestion[df_gestion['Categoria'] == 'redes'].copy()
    
    # Validamos si la consulta devuelve filas reales del Excel
    if not df_redes.empty and df_redes['Valor_Num'].sum() > 0:
        df_redes['Red_Social'] = df_redes['Item'].astype(str).str.capitalize()
        df_redes = df_redes.sort_values(by='Valor_Num', ascending=False)
        
        fig_redes = px.bar(
            df_redes,
            x='Red_Social',
            y='Valor_Num',
            title='Métricas de Seguidores Extraídas en Tiempo Real',
            color_discrete_sequence=['#475569'],
            template="plotly_white"
        )
        fig_redes.update_layout(plot_bgcolor='#ffffff', paper_bgcolor='#ffffff', height=350, font=dict(color="#000000"))
        fig_redes.update_yaxes(showgrid=True, gridcolor="#e2e8f0")
        st.plotly_chart(fig_redes, use_container_width=True)
    else:
        # En vez de pintar datos falsos si falla, notificamos al desarrollador
        st.warning("⚠️ No se detectaron registros válidos en la categoría 'redes' dentro de la pestaña 'Gestion_EI'.")
        st.markdown("**Estructura actual leída en memoria:**")
        st.dataframe(df_gestion)

st.markdown("---")
st.subheader("📅 Eventos Internacionales EULAC")
st.table(df_eventos)
