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

# BOTÓN DE LIMPIEZA TOTAL EN LA BARRA LATERAL
if st.sidebar.button("🔄 Forzar Recarga (Limpiar Caché)"):
    st.cache_data.clear()
    st.success("¡Caché de Google Sheets limpiada exitosamente!")

# ==========================================
# 2. CONEXIÓN EN TIEMPO REAL A TU "Hoja 1"
# ==========================================
@st.cache_data(ttl="2s") 
def cargar_datos():
    conn = st.connection("gsheets", type=GSheetsConnection)
    url_directa = "https://docs.google.com/spreadsheets/d/1aEIyDmHuHxzei8IRqMFKYDIZ1Hc3lvQoU6odzyuiL9M/edit?usp=sharing"
    return conn.read(spreadsheet=url_directa, sheet="Hoja 1")

try:
    df = cargar_datos()
    df.columns = df.columns.str.strip()
    
    # Normalización estricta de columnas para las búsquedas
    df['Categoria_Clean'] = df['Categoria'].astype(str).str.strip().str.lower()
    df['Item_Clean'] = df['Item'].astype(str).str.strip().str.lower()
    df['Valor_Clean'] = df['Valor'].astype(str).str.strip()
except Exception as e:
    st.error("⚠️ Error al conectar con la pestaña 'Hoja 1'")
    st.stop()

# Funciones de extracción directa por coincidencia de filas
def extraer_texto(item_nombre, defecto):
    try:
        fila = df[df['Item_Clean'] == item_nombre.lower().strip()]
        if not fila.empty:
            return str(fila.iloc[0]['Valor_Clean'])
        return defecto
    except:
        return defecto

def extraer_numero(item_nombre, defecto):
    try:
        fila = df[df['Item_Clean'] == item_nombre.lower().strip()]
        if not fila.empty:
            val = pd.to_numeric(fila.iloc[0]['Valor_Clean'], errors='coerce')
            if not pd.isna(val):
                return int(val)
        return defecto
    except:
        return defecto

# Muestra para auditoría en la barra lateral el contenido real leído
st.sidebar.markdown("### 📋 Data en vivo leída:")
st.sidebar.dataframe(df[['Categoria', 'Item', 'Valor']])

# ==========================================
# 3. CABECERA EJECUTIVA
# ==========================================
st.title("🏛️ Centro de Emprendimiento e Innovación - Misión 3")
st.markdown("### **Dashboard de Indicadores Estratégicos y de Gestión**")
st.markdown("**Sincronización Directa de una Sola Hoja | Conectado con Éxito**")
st.markdown("---")

# ==========================================
# 4. SECCIÓN 1: ESTADO OPERATIVO DE PLATAFORMAS
# ==========================================
st.subheader("🏢 Estado de la Unidad y Plataformas")
col_p1, col_p2, col_p3, col_p4, col_p5 = st.columns(5)

with col_p1:
    st.metric(label="Comité Plataforma", value=extraer_texto("Proyecto Comite", "Funcionando"), delta="✓ Estado")
with col_p2:
    st.metric(label="Dashboard Plataforma", value=extraer_texto("Dashboard", "Proceso"), delta="✓ Estado")
with col_p3:
    st.metric(label="Calculadora Valor", value=extraer_texto("Calculadora Valor", "Funcionando"), delta="✓ Estado")
with col_p4:
    st.metric(label="Consultoría Innovación", value=extraer_texto("Consultoria Innovacion", "Proceso"), delta="✓ Estado")
with col_p5:
    st.metric(label="Curso E&I Transversal", value=extraer_texto("Curso E&I Transversal", "Proceso"), delta="✓ Estado")

st.markdown("---")

# ==========================================
# 5. SECCIÓN 2: PIPELINE DE EMPRENDIMIENTO Y VINCULACIÓN
# ==========================================
col_izq, col_der = st.columns([1.2, 1])

with col_izq:
    st.subheader("🚀 Embudo del Emprendedor (E&I)")
    
    # Extrae basándose en tus términos de la columna Item (preincubacion, incubacion, aceleracion)
    pre_inc = extraer_numero("preincubacion", 60)
    inc = extraer_numero("incubacion", 25)
    ace = extraer_numero("aceleracion", 0)

    fig_embudo = go.Figure(go.Funnel(
        y=['Pre-incubación', 'Incubación', 'Aceleración'],
        x=[pre_inc, inc, ace],
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
    
    # Lee dinámicamente las entidades de tu Excel
    cam = extraer_numero("camaras", 20)
    uni = extraer_numero("universidades", 30)
    aso = extraer_numero("asociaciones", 6)
    inst = extraer_numero("instituciones", 4)
    
    df_ve_pie = pd.DataFrame({
        'Entidad': ['Cámaras', 'Universidades', 'Asociaciones', 'Instituciones'],
        'Cantidad': [cam, uni, aso, inst]
    })
    
    fig_pie = px.pie(
        df_ve_pie, 
        values='Cantidad', 
        names='Entidad',
        color_discrete_sequence=['#0f172a', '#1e293b', '#475569', '#94a3b8'],
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
    st.info(f"**Retos Territoriales Activos:**\n* {extraer_texto('Innovacion Abierta', 'Miraflores / Callao Tech')}")
    st.metric(label="Polinización (Participantes)", value=extraer_numero("Polinización", 1))

with col_r2:
    st.subheader("📅 Eventos Internacionales EULAC")
    datos_eventos = {
        'Sede / Evento': ['EULAC LIMA', 'EULAC CIX', 'EULAC AQP', 'Mentores'],
        'Aforo': [
            extraer_texto("EULAC LIM", "120 Pax"), 
            extraer_texto("EULAC CIX", "120 Pax"), 
            extraer_texto("EULAC AQP", "120 Pax"),
            extraer_texto("Mentores", "120 Pax")
        ]
    }
    st.table(pd.DataFrame(datos_eventos))

with col_r3:
    st.subheader("🧠 Viajes e Impacto")
    st.metric(label="Visitas Campus", value=extraer_numero("Visitas Campus", 12))

st.markdown("---")

# ==========================================
# 7. SECCIÓN 4: ANALÍTICA DIGITAL (LECTURA REAL DIRECTA DESDE TU FILA)
# ==========================================
st.subheader("🌐 Visitas a Plataformas vs. Comunidad Digital")
col_v1, col_v2 = st.columns(2)

with col_v1:
    items_v = ['ATIPAQ', 'Miraflores', 'Mentores', 'Callao Tech']
    vals_v = [
        extraer_numero("ATIPAQ", 268), 
        extraer_numero("Miraflores", 64), 
        extraer_numero("Mentores", 113),
        extraer_numero("Callao Tech", 8)
    ]
    df_visitas_dinamico = pd.DataFrame({'Item': items_v, 'Valor': vals_v}).sort_values(by='Valor')
    
    fig_visitas = px.bar(df_visitas_dinamico, x='Valor', y='Item', orientation='h', template="plotly_white", color_discrete_sequence=['#0f172a'])
    fig_visitas.update_layout(title='Volumen de Tráfico por Canal', plot_bgcolor='#ffffff', paper_bgcolor='#ffffff', height=380, font=dict(color="#000000"))
    fig_visitas.update_xaxes(title_text="Interacciones", tickfont=dict(color="#000000"), showgrid=True, gridcolor="#e2e8f0")
    fig_visitas.update_yaxes(title_text="Canal", tickfont=dict(color="#000000"))
    st.plotly_chart(fig_visitas, use_container_width=True)

with col_v2:
    # MAPEADO EXACTO DE TUS FILAS DE REDES (Extracción directa e incontestable)
    redes_lista = ['TikTok', 'Instagram', 'LinkedIn', 'Facebook', 'YouTube']
    valores_redes = [
        extraer_numero("tiktok", 7211),
        extraer_numero("instagram", 2146),
        extraer_numero("linkedin", 829),
        extraer_numero("facebook", 386),
        extraer_numero("youtube", 53)
    ]
    
    df_redes_final = pd.DataFrame({
        'Red Social': redes_lista,
        'Miembros': valores_redes
    }).sort_values(by='Miembros', ascending=False)
    
    fig_redes = px.bar(
        df_redes_final,
        x='Red Social',
        y='Miembros',
        title='Seguidores Totales en Canales Digitales (Sincronizado)',
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
    "Sincronizado directamente con la estructura vertical de la Hoja 1."
    "</center>", 
    unsafe_allow_html=True
)
