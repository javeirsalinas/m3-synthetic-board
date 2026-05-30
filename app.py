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

st.markdown("""
    <style>
    .main, [data-testid="stAppViewContainer"], [data-testid="stHeader"] { 
        background-color: #ffffff !important; 
    }
    div[data-testid="metric-container"] {
        background-color: #ffffff !important;
        border-top: 4px solid #1e293b !important;
        border-left: 1px solid #cbd5e1 !important;
        border-right: 1px solid #cbd5e1 !important;
        border-bottom: 1px solid #cbd5e1 !important;
        padding: 20px !important;
        border-radius: 8px !important;
        box-shadow: 0 2px 8px rgba(0, 0, 0, 0.05) !important;
    }
    [data-testid="stMetricValue"] { font-size: 30px !important; color: #000000 !important; font-weight: 700 !important; }
    [data-testid="stMetricLabel"] { font-size: 14px !important; color: #0f172a !important; font-weight: 600 !important; }
    h1, h2, h3, h4, h5, h6 { color: #000000 !important; font-family: Arial, sans-serif; }
    p, span, li, td, th { color: #000000 !important; }
    .stAlert { background-color: #f1f5f9 !important; border: 1px solid #cbd5e1 !important; }
    </style>
    """, unsafe_allow_html=True)

# ==========================================
# 2. CONEXIÓN EN TIEMPO REAL A GOOGLE SHEETS
# ==========================================
@st.cache_data(ttl="1m") # Reducido a 1 minuto para actualizaciones más rápidas
def cargar_datos():
    conn = st.connection("gsheets", type=GSheetsConnection)
    url_directa = "https://docs.google.com/spreadsheets/d/1aEIyDmHuHxzei8IRqMFKYDIZ1Hc3lvQoU6odzyuiL9M/edit?usp=sharing"
    return conn.read(spreadsheet=url_directa)

try:
    df = cargar_datos()
    # Limpieza básica por si hay espacios vacíos en el Excel
    df.columns = df.columns.str.strip()
    df['Categoria'] = df['Categoria'].astype(str).str.strip().str.upper()
    df['Item'] = df['Item'].astype(str).str.strip()
except Exception as e:
    st.error("⚠️ Error al leer o procesar la estructura de Google Sheets")
    st.stop()

# Función auxiliar para extraer valores dinámicamente del Excel
def obtener_valor(item_nombre, valor_defecto):
    try:
        fila = df[df['Item'] == item_nombre]
        if not fila.empty:
            return fila.iloc[0]['Valor']
        return valor_defecto
    except:
        return valor_defecto

# ==========================================
# 3. CABECERA EJECUTIVA
# ==========================================
st.title("🏛️ Centro de Emprendimiento e Innovación - Misión 3")
st.markdown("### **Dashboard de Indicadores Estratégicos y de Gestión**")
st.markdown("**Reporte gerencial automatizado en tiempo real | Conectado a Google Sheets**")
st.markdown("---")

# ==========================================
# 4. SECCIÓN 1: ESTADO OPERATIVO DE PLATAFORMAS (DINÁMICO)
# ==========================================
st.subheader("🏢 Estado de la Unidad y Plataformas")
col_p1, col_p2, col_p3, col_p4, col_p5 = st.columns(5)

with col_p1:
    st.metric(label="Comité Plataforma", value=obtener_valor("Comité Plataforma", "Funcionando"), delta="✓ Estado")
with col_p2:
    st.metric(label="Dashboard Plataforma", value=obtener_valor("Dashboard Plataforma", "Funcionando"), delta="✓ Estado")
with col_p3:
    st.metric(label="Calculadora Valor", value=obtener_valor("Calculadora Valor", "Funcionando"), delta="✓ Estado")
with col_p4:
    st.metric(label="Consultoría Innovación", value=obtener_valor("Consultoría Innovación", "Proyecto"), delta="✓ Estado")
with col_p5:
    st.metric(label="Curso E&I Transversal", value=obtener_valor("Curso E&I Transversal", "Proyecto"), delta="✓ Estado")

st.markdown("---")

# ==========================================
# 5. SECCIÓN 2: PIPELINE DE EMPRENDIMIENTO Y VINCULACIÓN (DINÁMICO)
# ==========================================
col_izq, col_der = st.columns([1.2, 1])

with col_izq:
    st.subheader("🚀 Embudo del Emprendedor (E&I)")
    
    # Extraemos los participantes directo de la columna 'Valor' del Excel
    pre_inc = pd.to_numeric(obtener_valor("Pre-incubación", 60), errors='coerce')
    inc = pd.to_numeric(obtener_valor("Incubación", 25), errors='coerce')
    aceleracion = pd.to_numeric(obtener_valor("Aceleración", 0), errors='coerce')

    fig_embudo = go.Figure(go.Funnel(
        y=['Pre-incubación', 'Incubación', 'Aceleración'],
        x=[pre_inc, inc, aceleracion],
        textinfo="value+percent initial",
        marker={
            "color": ["#0f172a", "#334155", "#64748b"],
            "line": {"width": 1, "color": "#cbd5e1"}
        },
        textfont=dict(color="#ffffff", size=12)
    ))
    fig_embudo.update_layout(
        template="plotly_white",
        margin=dict(l=120, r=40, t=20, b=20), 
        height=380,
        plot_bgcolor='#ffffff',
        paper_bgcolor='#ffffff',
        font=dict(color="#000000", size=13)
    )
    fig_embudo.update_yaxes(tickfont=dict(color="#000000", size=13, family="Arial, sans-serif"))
    st.plotly_chart(fig_embudo, use_container_width=True)

with col_der:
    st.subheader("🤝 Ecosistema de Vinculación (V&E)")
    
    # Filtramos la categoría V&E directamente de la tabla Excel
    df_ve = df[df['Categoria'] == 'V&E'].copy()
    df_ve['Valor'] = pd.to_numeric(df_ve['Valor'], errors='coerce')
    
    # Si por algún motivo el filtro está vacío, usa los datos de respaldo
    if df_ve.empty:
        df_ve = pd.DataFrame({
            'Item': ['Universidades', 'Incubadoras', 'Cámaras', 'Asociaciones', 'Instituciones'],
            'Valor': [20, 20, 19, 6, 4]
        })
    
    fig_pie = px.pie(
        df_ve, 
        values='Valor', 
        names='Item',
        color_discrete_sequence=['#0f172a', '#1e293b', '#475569', '#94a3b8', '#cbd5e1'],
        template="plotly_white"
    )
    fig_pie.update_layout(
        margin=dict(l=20, r=20, t=20, b=20), 
        height=380,
        plot_bgcolor='#ffffff',
        paper_bgcolor='#ffffff',
        legend=dict(orientation="h", yanchor="bottom", y=-0.15, xanchor="center", x=0.5, font=dict(color="#000000", size=11))
    )
    st.plotly_chart(fig_pie, use_container_width=True)

st.markdown("---")

# ==========================================
# 6. SECCIÓN 3: RETOS, EVENTOS Y MENTORES (DINÁMICO)
# ==========================================
col_r1, col_r2, col_r3 = st.columns(3)

with col_r1:
    st.subheader("🎯 Innovación Abierta y Retos")
    st.info("**Retos Territoriales Activos:**\n* Miraflores\n* Callao Tech")
    st.metric(label="Innovación Abierta EU (Participantes)", value=obtener_valor("Innovación Abierta EU", "1"))
    st.metric(label="Polinización (Participantes)", value=obtener_valor("Polinización", "1"))

with col_r2:
    st.subheader("📅 Eventos Internacionales EULAC")
    datos_eventos = {
        'Sede / Evento': ['EULAC LIMA', 'EULAC CIX', 'EULAC AQP'],
        'Aforo Alcanzado': [obtener_valor("EULAC LIM", "120 Pax"), obtener_valor("EULAC CIX", "120 Pax"), obtener_valor("EULAC AQP", "120 Pax")]
    }
    st.table(pd.DataFrame(datos_eventos))

with col_r3:
    st.subheader("🧠 Capital Intelectual")
    st.metric(label="Red Global de Mentores", value=obtener_valor("Mentores", "120 Pax"), delta="Estrategas")

st.markdown("---")

# ==========================================
# 7. SECCIÓN 4: ANALÍTICA DIGITAL Y REDES (DINÁMICO)
# ==========================================
st.subheader("🌐 Visitas a Plataformas vs. Comunidad Digital")
col_v1, col_v2 = st.columns(2)

with col_v1:
    # Filtramos las visitas de plataformas directamente desde el Excel
    df_visitas = df[df['Categoria'] == 'VISITAS'].copy()
    df_visitas['Valor'] = pd.to_numeric(df_visitas['Valor'], errors='coerce')
    df_visitas = df_visitas.dropna(subset=['Valor']).sort_values(by='Valor')
    
    if df_visitas.empty:
        df_visitas = pd.DataFrame({
            'Item': ['ATIPAQ', 'Mentores', 'Miraflores', 'Pre-incubación', 'Incubación', 'Callao Tech'],
            'Valor': [243, 114, 64, 60, 25, 7]
        }).sort_values(by='Valor')
    
    fig_visitas = px.bar(
        df_visitas, 
        x='Valor', 
        y='Item', 
        orientation='h',
        title='Volumen de Tráfico y Participación por Canal',
        color_discrete_sequence=['#0f172a'],
        template="plotly_white"
    )
    fig_visitas.update_layout(plot_bgcolor='#ffffff', paper_bgcolor='#ffffff', height=400, font=dict(color="#000000"))
    fig_visitas.update_xaxes(title_text="Interacciones", tickfont=dict(color="#000000"), showgrid=True, gridcolor="#e2e8f0")
    fig_visitas.update_yaxes(title_text="Canal", tickfont=dict(color="#000000"))
    st.plotly_chart(fig_visitas, use_container_width=True)

with col_v2:
    # Filtramos las redes sociales directamente desde el Excel
    df_redes = df[df['Categoria'] == 'REDES'].copy()
    df_redes['Valor'] = pd.to_numeric(df_redes['Valor'], errors='coerce')
    df_redes = df_redes.dropna(subset=['Valor']).sort_values(by='Valor', ascending=False)
    
    if df_redes.empty:
        df_redes = pd.DataFrame({
            'Item': ['TikTok', 'Instagram', 'Facebook', 'LinkedIn', 'YouTube'],
            'Valor': [3000, 2000, 2000, 1000, 200]
        })
    
    fig_redes = px.bar(
        df_redes,
        x='Item',
        y='Valor',
        title='Seguidores Totales en Canales Digitales',
        color_discrete_sequence=['#475569'],
        template="plotly_white"
    )
    fig_redes.update_layout(plot_bgcolor='#ffffff', paper_bgcolor='#ffffff', height=400, font=dict(color="#000000"))
    fig_redes.update_xaxes(title_text="Red Social", tickfont=dict(color="#000000"))
    fig_redes.update_yaxes(title_text="Miembros", tickfont=dict(color="#000000"), showgrid=True, gridcolor="#e2e8f0")
    st.plotly_chart(fig_redes, use_container_width=True)

# ==========================================
# 8. PIE DE PÁGINA
# ==========================================
st.markdown("---")
st.markdown(
    "<center style='color: #000000; font-size: 14px; font-weight: 600;'> "
    "© Misión 3 - Centro de Emprendimiento e Innovación | Universidad César Vallejo<br>"
    "Infraestructura Cloud conectada automáticamente mediante canales analíticos distribuidos."
    "</center>", 
    unsafe_allow_html=True
)
