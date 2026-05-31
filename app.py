import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from streamlit_gsheets import GSheetsConnection

# ==========================================
# 1. CONFIGURACIÓN DE LA PÁGINA Y UX/UI
# ==========================================
st.set_page_config(
    page_title="Misión 3 - Dashboard Ejecutivo",
    page_icon="🏛️",
    layout="wide"
)

# Inyección de CSS para garantizar el diseño claro elegante y letras negras de alto contraste
st.markdown("""
    <style>
    /* Fondo principal de la aplicación y contenedores web */
    .main, [data-testid="stAppViewContainer"], [data-testid="stHeader"] { 
        background-color: #ffffff !important; 
    }
    
    /* Diseño de tarjetas KPIs (Fondo blanco brillante con bordes finos en gris) */
    div[data-testid="metric-container"] {
        background-color: #ffffff !important;
        border-top: 4px solid #0f172a !important; /* Línea superior negra corporativa */
        border-left: 1px solid #cbd5e1 !important;
        border-right: 1px solid #cbd5e1 !important;
        border-bottom: 1px solid #cbd5e1 !important;
        padding: 20px !important;
        border-radius: 8px !important;
        box-shadow: 0 4px 10px rgba(0, 0, 0, 0.02) !important;
    }
    
    /* Textos principales de las métricas en negro estricto */
    [data-testid="stMetricValue"] { 
        font-size: 30px !important; 
        color: #000000 !important; 
        font-weight: 700 !important; 
    }
    [data-testid="stMetricLabel"] { 
        font-size: 14px !important; 
        color: #334155 !important; 
        font-weight: 600 !important; 
    }
    
    /* Configuración de títulos tipográficos en negro */
    h1 { 
        color: #000000 !important; 
        font-family: 'Helvetica Neue', Arial, sans-serif; 
        font-weight: 700; 
    }
    h2, h3 { 
        color: #0f172a !important; 
        font-family: Arial, sans-serif; 
        font-weight: 600; 
    }
    
    /* Forzar todos los textos secundarios y tablas a color negro absoluto */
    p, span, li, td, th {
        color: #000000 !important;
    }
    
    .stTable {
        background-color: #ffffff !important;
    }
    </style>
    """, unsafe_allow_html=True)

# BOTÓN EN LA BARRA LATERAL PARA BORRAR CACHÉ INSTANTÁNEAMENTE
if st.sidebar.button("🔄 Forzar Recarga (Limpiar Caché)"):
    st.cache_data.clear()
    st.success("¡Caché de Google Sheets limpiada exitosamente!")

# ==========================================
# 2. CONEXIÓN OPTIMIZADA A LAS NUEVAS PESTAÑAS
# ==========================================
url_directa = "https://docs.google.com/spreadsheets/d/1aEIyDmHuHxzei8IRqMFKYDIZ1Hc3lvQoU6odzyuiL9M/edit?usp=sharing"

@st.cache_data(ttl="10m") # Guardado en caché por 10 minutos para velocidad máxima
def cargar_pestana(nombre_pestana):
    conn = st.connection("gsheets", type=GSheetsConnection)
    return conn.read(spreadsheet=url_directa, sheet=nombre_pestana)

try:
    # Descarga directa de los 3 bloques estructurados de datos
    df_plataformas = cargar_pestana("Plataformas")
    df_gestion = cargar_pestana("Gestion_EI")
    df_eventos = cargar_pestana("Eventos_EULAC")
    
    # Limpieza estándar preventiva de textos
    df_plataformas.columns = df_plataformas.columns.str.strip()
    df_gestion.columns = df_gestion.columns.str.strip()
    df_eventos.columns = df_eventos.columns.str.strip()
    
    df_gestion['Categoria'] = df_gestion['Categoria'].astype(str).str.strip().str.lower()
    df_gestion['Valor'] = pd.to_numeric(df_gestion['Valor'], errors='coerce')
except Exception as e:
    st.error("⚠️ Error al conectar u organizar las nuevas pestañas del Google Sheet")
    st.info("Asegúrate de que los nombres de las pestañas sean exactamente: 'Plataformas', 'Gestion_EI' y 'Eventos_EULAC'.")
    st.stop()

# ==========================================
# 3. CABECERA EJECUTIVA INSTITUCIONAL
# ==========================================
st.title("🏛️ Centro de Emprendimiento e Innovación - Misión 3")
st.markdown("### **Dashboard de Indicadores Estratégicos y de Gestión**")
st.caption("Reporte gerencial automatizado conectado en tiempo real con bases de datos relacionales")
st.markdown("---")

# ==========================================
# 4. SECCIÓN 1: ESTADO OPERATIVO DE PLATAFORMAS (DINÁMICO)
# ==========================================
st.subheader("🏢 Estado de la Unidad y Plataformas")
cols_plat = st.columns(len(df_plataformas))

for index, row in df_plataformas.iterrows():
    with cols_plat[index % len(df_plataformas)]:
        st.metric(label=str(row['Plataforma']), value=str(row['Estado']), delta="✓ Monitoreo")

st.markdown("---")

# ==========================================
# 5. SECCIÓN 2: PIPELINE DE EMPRENDIMIENTO Y VINCULACIÓN (DINÁMICO)
# ==========================================
col_izq, col_der = st.columns([1.2, 1])

with col_izq:
    st.subheader("🚀 Embudo del Emprendedor (E&I)")
    # Filtrado directo de la categoría programa
    df_embudo = df_gestion[df_gestion['Categoria'] == 'programa'].copy()
    
    fig_embudo = go.Figure(go.Funnel(
        y=df_embudo['Item'],
        x=df_embudo['Valor'],
        textinfo="value+percent initial",
        marker={
            "color": ["#0f172a", "#334155", "#64748b"],
            "line": {"width": 1, "color": "#cbd5e1"}
        },
        textfont=dict(color="#ffffff", size=12)
    ))
    fig_embudo.update_layout(
        template="plotly_white",
        margin=dict(l=140, r=40, t=20, b=20), 
        height=350,
        plot_bgcolor='#ffffff',
        paper_bgcolor='#ffffff',
        font=dict(color="#000000", size=13)
    )
    fig_embudo.update_yaxes(tickfont=dict(color="#000000", size=13, family="Arial, sans-serif"))
    st.plotly_chart(fig_embudo, use_container_width=True)

with col_der:
    st.subheader("🤝 Ecosistema de Vinculación (V&E)")
    # Filtrado directo de la categoría entidades para el gráfico circular
    df_entidades = df_gestion[df_gestion['Categoria'] == 'entidades'].copy()
    
    fig_pie = px.pie(
        df_entidades, 
        values='Valor', 
        names='Item',
        color_discrete_sequence=['#0f172a', '#1e293b', '#475569', '#94a3b8', '#cbd5e1'],
        template="plotly_white"
    )
    fig_pie.update_layout(
        margin=dict(l=20, r=20, t=20, b=20), 
        height=350,
        plot_bgcolor='#ffffff',
        paper_bgcolor='#ffffff',
        legend=dict(orientation="h", yanchor="bottom", y=-0.15, xanchor="center", x=0.5, font=dict(color="#000000", size=11))
    )
    st.plotly_chart(fig_pie, use_container_width=True)

st.markdown("---")

# ==========================================
# 6. SECCIÓN 3: RETOS Y EVENTOS
# ==========================================
col_r1, col_r2 = st.columns([1, 2])

with col_r1:
    st.subheader("🎯 Innovación Abierta")
    st.info("**Retos Territoriales Activos:**\n* Miraflores\n* Callao Tech")
    
    # Extrae el participante de polinización si existe en la tabla
    df_polinizacion = df_gestion[df_gestion['Item'].str.lower() == 'polinización']
    val_pol = int(df_polinizacion.iloc[0]['Valor']) if not df_polinizacion.empty else 1
    st.metric(label="Polinización (Participantes)", value=val_pol)

with col_r2:
    st.subheader("📅 Eventos Internacionales EULAC")
    # Muestra de forma limpia y directa la tabla de eventos de la pestaña 3
    st.table(df_eventos)

st.markdown("---")

# ==========================================
# 7. SECCIÓN 4: ANALÍTICA DIGITAL Y TRAFICO (DINÁMICO)
# ==========================================
st.subheader("🌐 Visitas a Plataformas vs. Comunidad Digital")
col_v1, col_v2 = st.columns(2)

with col_v1:
    # Filtrado directo de tráfico de plataformas
    df_visitas = df_gestion[df_gestion['Categoria'] == 'trafico'].copy().sort_values(by='Valor')
    
    fig_visitas = px.bar(
        df_visitas, 
        x='Valor', 
        y='Item', 
        orientation='h', 
        template="plotly_white", 
        color_discrete_sequence=['#0f172a']
    )
    fig_visitas.update_layout(title='Volumen de Tráfico por Canal', plot_bgcolor='#ffffff', paper_bgcolor='#ffffff', height=380, font=dict(color="#000000"))
    fig_visitas.update_xaxes(title_text="Interacciones", tickfont=dict(color="#000000"), showgrid=True, gridcolor="#e2e8f0")
    fig_visitas.update_yaxes(title_text="Canal", tickfont=dict(color="#000000"))
    st.plotly_chart(fig_visitas, use_container_width=True)

with col_v2:
    # Filtrado directo y limpio de las Redes Sociales
    df_redes = df_gestion[df_gestion['Categoria'] == 'redes'].copy().sort_values(by='Valor', ascending=False)
    
    fig_redes = px.bar(
        df_redes,
        x='Item',
        y='Valor',
        title='Seguidores Totales en Canales Digitales',
        color_discrete_sequence=['#475569'],
        template="plotly_white"
    )
    fig_redes.update_layout(plot_bgcolor='#ffffff', paper_bgcolor='#ffffff', height=380, font=dict(color="#000000"))
    fig_redes.update_xaxes(title_text="Red Social", tickfont=dict(color="#000000"))
    fig_redes.update_yaxes(title_text="Miembros", tickfont=dict(color="#000000"), showgrid=True, gridcolor="#e2e8f0")
    st.plotly_chart(fig_redes, use_container_width=True)

# ==========================================
# 8. PIE DE PÁGINA CORPORATIVO
# ==========================================
st.markdown("---")
st.markdown(
    "<center style='color: #000000; font-size: 14px; font-weight: 600;'> "
    "© Misión 3 - Centro de Emprendimiento e Innovación | Universidad César Vallejo<br>"
    "Infraestructura optimizada mediante arquitectura de bases de datos distribuidas por pestañas."
    "</center>", 
    unsafe_allow_html=True
)
