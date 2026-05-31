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
# 2. CONEXIÓN DIRECTA A LA PESTAÑA "Hoja 1"
# ==========================================
@st.cache_data(ttl="5s") 
def cargar_datos():
    conn = st.connection("gsheets", type=GSheetsConnection)
    url_directa = "https://docs.google.com/spreadsheets/d/1aEIyDmHuHxzei8IRqMFKYDIZ1Hc3lvQoU6odzyuiL9M/edit?usp=sharing"
    # SOLUCIÓN CLAVE: Apuntamos exactamente al nombre de tu pestaña 'Hoja 1'
    return conn.read(spreadsheet=url_directa, worksheet="Hoja 1")

try:
    df = cargar_datos()
    # Limpieza de espacios en blanco en las cabeceras y celdas
    df.columns = df.columns.str.strip()
    df['Categoria'] = df['Categoria'].astype(str).str.strip().str.lower()
    df['Item'] = df['Item'].astype(str).str.strip()
    df['Valor_Num'] = pd.to_numeric(df['Valor'], errors='coerce')
except Exception as e:
    st.error("⚠️ Error al procesar la pestaña 'Hoja 1' de Google Sheets")
    st.stop()

# Funciones de extracción directa basadas en tu captura
def extraer_valor_kpi(item_buscado, defecto):
    try:
        sub_df = df[df['Item'].str.lower() == item_buscado.lower()]
        if not sub_df.empty:
            return str(sub_df.iloc[0]['Valor'])
        return defecto
    except:
        return defecto

def extraer_numero_kpi(item_buscado, defecto):
    try:
        sub_df = df[df['Item'].str.lower() == item_buscado.lower()]
        if not sub_df.empty:
            val = sub_df.iloc[0]['Valor_Num']
            if not pd.isna(val):
                return int(val)
        return defecto
    except:
        return defecto

# ==========================================
# 3. CABECERA EJECUTIVA
# ==========================================
st.title("🏛️ Centro de Emprendimiento e Innovación - Misión 3")
st.markdown("### **Dashboard de Indicadores Estratégicos y de Gestión**")
st.markdown("**Reporte gerencial conectado en tiempo real con 'Hoja 1'**")
st.markdown("---")

# ==========================================
# 4. SECCIÓN 1: ESTADO OPERATIVO DE PLATAFORMAS
# ==========================================
st.subheader("🏢 Estado de la Unidad y Plataformas")
col_p1, col_p2, col_p3, col_p4, col_p5 = st.columns(5)

with col_p1:
    st.metric(label="Comité Plataforma", value=extraer_valor_kpi("Proyecto Comite", "Funcionando"), delta="✓ Estado")
with col_p2:
    st.metric(label="Dashboard Plataforma", value=extraer_valor_kpi("Dashboard", "Proceso"), delta="✓ Estado")
with col_p3:
    st.metric(label="Calculadora Valor", value=extraer_valor_kpi("Calculadora Valor", "Funcionando"), delta="✓ Estado")
with col_p4:
    st.metric(label="Consultoría Innovación", value=extraer_valor_kpi("Consultoria Innovacion", "Proceso"), delta="✓ Estado")
with col_p5:
    st.metric(label="Curso E&I Transversal", value=extraer_valor_kpi("Curso E&I Transversal", "Proceso"), delta="✓ Estado")

st.markdown("---")

# ==========================================
# 5. SECCIÓN 2: PIPELINE DE EMPRENDIMIENTO Y VINCULACIÓN
# ==========================================
col_izq, col_der = st.columns([1.2, 1])

with col_izq:
    st.subheader("🚀 Embudo del Emprendedor (E&I)")
    
    # Extrae los participantes directo de las filas 8, 9 y 10 de tu captura
    pre_inc = extraer_numero_kpi("Preincubacion", 60)
    inc = extraer_numero_kpi("Incubacion", 25)
    aceleracion = extraer_numero_kpi("Aceleracion", 0)

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
        height=350,
        plot_bgcolor='#ffffff',
        paper_bgcolor='#ffffff',
        font=dict(color="#000000", size=13)
    )
    fig_embudo.update_yaxes(tickfont=dict(color="#000000", size=13, family="Arial, sans-serif"))
    st.plotly_chart(fig_embudo, use_container_width=True)

with col_der:
    st.subheader("🤝 Ecosistema de Vinculación (V&E)")
    
    # Mapea dinámicamente las filas de la categoría 'entidades' (filas 15 a 18)
    df_ve = df[df['Categoria'] == 'entidades'].copy()
    
    if not df_ve.empty:
        fig_pie = px.pie(
            df_ve, 
            values='Valor_Num', 
            names='Item',
            color_discrete_sequence=['#0f172a', '#1e293b', '#475569', '#94a3b8', '#cbd5e1'],
            template="plotly_white"
        )
    else:
        fig_pie = px.pie(
            names=['Camaras', 'Universidades', 'Asociaciones', 'Instituciones'],
            values=[20, 30, 6, 4],
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
col_r1, col_r2, col_r3 = st.columns(3)

with col_r1:
    st.subheader("🎯 Innovación Abierta")
    st.info(f"**Retos Territoriales Activos:**\n* {extraer_valor_kpi('Innovacion Abierta', 'Miraflores')}")
    st.metric(label="Polinización (Participantes)", value=extraer_numero_kpi("Polinización", 1))

with col_r2:
    st.subheader("📅 Eventos Internacionales EULAC")
    datos_eventos = {
        'Sede / Evento': ['EULAC LIMA', 'EULAC CIX', 'EULAC AQP', 'Mentores'],
        'Aforo Alcanzado': [
            extraer_valor_kpi("EULAC LIM", "120 Pax"), 
            extraer_valor_kpi("EULAC CIX", "120 Pax"), 
            extraer_valor_kpi("EULAC AQP", "120 Pax"),
            extraer_valor_kpi("Mentores", "120 Pax")
        ]
    }
    st.table(pd.DataFrame(datos_eventos))

with col_r3:
    st.subheader("🧠 Viajes e Impacto")
    st.metric(label="Visitas Campus", value=extraer_numero_kpi("Visitas Campus", 12))

st.markdown("---")

# ==========================================
# 7. SECCIÓN 4: ANALÍTICA DIGITAL (REDES SOCIALES CORREGIDAS)
# ==========================================
st.subheader("🌐 Visitas a Plataformas vs. Comunidad Digital")
col_v1, col_v2 = st.columns(2)

with col_v1:
    # Mapeo de visitas reales de tus filas de participantes (ATIPAQ, Callao Tech, Miraflores)
    items_v = ['ATIPAQ', 'Miraflores', 'Mentores', 'Callao Tech']
    vals_v = [
        extraer_numero_kpi("ATIPAQ", 268), 
        extraer_numero_kpi("Miraflores", 64), 
        extraer_numero_kpi("Mentores", 113),
        extraer_numero_kpi("Callao Tech", 8)
    ]
    df_visitas_dinamico = pd.DataFrame({'Item': items_v, 'Valor': vals_v}).sort_values(by='Valor')
    
    fig_visitas = px.bar(df_visitas_dinamico, x='Valor', y='Item', orientation='h', template="plotly_white", color_discrete_sequence=['#0f172a'])
    fig_visitas.update_layout(title='Volumen de Tráfico por Canal', plot_bgcolor='#ffffff', paper_bgcolor='#ffffff', height=380, font=dict(color="#000000"))
    fig_visitas.update_xaxes(title_text="Interacciones", tickfont=dict(color="#000000"), showgrid=True, gridcolor="#e2e8f0")
    fig_visitas.update_yaxes(title_text="Canal", tickfont=dict(color="#000000"))
    st.plotly_chart(fig_visitas, use_container_width=True)

with col_v2:
    # FILTRADO EXACTO BASADO EN TU CAPTURA (FILAS 30 A 34)
    df_redes = df[df['Categoria'] == 'miembros'].copy()
    
    if not df_redes.empty and df_redes['Valor_Num'].sum() > 0:
        df_redes = df_redes.dropna(subset=['Valor_Num']).sort_values(by='Valor_Num', ascending=False)
        fig_redes = px.bar(
            df_redes,
            x='Item',
            y='Valor_Num',
            title='Seguidores Totales en Canales Digitales (Datos de Hoja 1)',
            color_discrete_sequence=['#475569'],
            template="plotly_white"
        )
    else:
        # Respaldo con tus datos exactos por si acaso
        fig_redes = px.bar(
            x=['TikTok', 'Instagram', 'Linkedin', 'Facebook', 'YouTube'],
            y=[7211, 2146, 829, 386, 53],
            title='Seguidores Totales en Canales Digitales (Respaldo)',
            color_discrete_sequence=['#475569'],
            template="plotly_white"
        )
        
    fig_redes.update_layout(plot_bgcolor='#ffffff', paper_bgcolor='#ffffff', height=380, font=dict(color="#000000"))
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
    "Sincronizado con la pestaña 'Hoja 1' del Google Sheet Institucional."
    "</center>", 
    unsafe_allow_html=True
)
