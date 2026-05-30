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
@st.cache_data(ttl="10s") # Bajado a 10 segundos para ver cambios casi instantáneos
def cargar_datos():
    conn = st.connection("gsheets", type=GSheetsConnection)
    url_directa = "https://docs.google.com/spreadsheets/d/1aEIyDmHuHxzei8IRqMFKYDIZ1Hc3lvQoU6odzyuiL9M/edit?usp=sharing"
    return conn.read(spreadsheet=url_directa)

try:
    df = cargar_datos()
    # Limpieza rigurosa para evitar errores por espacios o mayúsculas
    df.columns = df.columns.str.strip()
    df['Categoria_Limpia'] = df['Categoria'].astype(str).str.strip().str.upper()
    df['Item_Limpio'] = df['Item'].astype(str).str.strip().str.lower()
    df['Valor_Numerico'] = pd.to_numeric(df['Valor'], errors='coerce')
except Exception as e:
    st.error("⚠️ Error al procesar la estructura de Google Sheets")
    st.stop()

# Función de búsqueda flexible (ignora mayúsculas, minúsculas y espacios)
def buscar_valor_flexible(subcadena, valor_defecto, es_numerico=False):
    try:
        subcadena = subcadena.lower().strip()
        coincidencia = df[df['Item_Limpio'].str.contains(subcadena, na=False)]
        if not coincidencia.empty:
            if es_numerico:
                return coincidencia.iloc[0]['Valor_Numerico']
            return coincidencia.iloc[0]['Valor']
        return valor_defecto
    except:
        return valor_defecto

# ==========================================
# 3. CABECERA EJECUTIVA
# ==========================================
st.title("🏛️ Centro de Emprendimiento e Innovación - Misión 3")
st.markdown("### **Dashboard de Indicadores Estratégicos y de Gestión**")
st.markdown("**Reporte gerencial automatizado en tiempo real | Sincronización Flexible**")
st.markdown("---")

# ==========================================
# 4. SECCIÓN 1: ESTADO OPERATIVO DE PLATAFORMAS
# ==========================================
st.subheader("🏢 Estado de la Unidad y Plataformas")
col_p1, col_p2, col_p3, col_p4, col_p5 = st.columns(5)

with col_p1:
    st.metric(label="Comité Plataforma", value=buscar_valor_flexible("comité", "Funcionando"), delta="✓ Estado")
with col_p2:
    st.metric(label="Dashboard Plataforma", value=buscar_valor_flexible("dashboard", "Funcionando"), delta="✓ Estado")
with col_p3:
    st.metric(label="Calculadora Valor", value=buscar_valor_flexible("calculadora", "Funcionando"), delta="✓ Estado")
with col_p4:
    st.metric(label="Consultoría Innovación", value=buscar_valor_flexible("consultoría", "Proyecto"), delta="✓ Estado")
with col_p5:
    st.metric(label="Curso E&I Transversal", value=buscar_valor_flexible("curso", "Proyecto"), delta="✓ Estado")

st.markdown("---")

# ==========================================
# 5. SECCIÓN 2: PIPELINE DE EMPRENDIMIENTO Y VINCULACIÓN
# ==========================================
col_izq, col_der = st.columns([1.2, 1])

with col_izq:
    st.subheader("🚀 Embudo del Emprendedor (E&I)")
    
    # Búsqueda automatizada de las fases del embudo
    pre_inc = buscar_valor_flexible("pre-incubación", 60, es_numerico=True)
    # Si no lo encuentra por guion, intenta buscar por espacio
    if pd.isna(pre_inc) or pre_inc == 60:
        pre_inc = buscar_valor_flexible("pre incubación", 60, es_numerico=True)
        
    inc = buscar_valor_flexible("incubación", 25, es_numerico=True)
    aceleracion = buscar_valor_flexible("aceleración", 0, es_numerico=True)

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
    
    # Extrae dinámicamente todo lo marcado como V&E en tu Excel
    df_ve = df[df['Categoria_Limpia'] == 'V&E'].copy()
    
    if not df_ve.empty:
        fig_pie = px.pie(
            df_ve, 
            values='Valor_Numerico', 
            names='Item',
            color_discrete_sequence=['#0f172a', '#1e293b', '#475569', '#94a3b8', '#cbd5e1'],
            template="plotly_white"
        )
    else:
        # Respaldo por si la categoría no está escrita tal cual
        fig_pie = px.pie(
            names=['Universidades', 'Incubadoras', 'Cámaras', 'Asociaciones', 'Instituciones'],
            values=[20, 20, 19, 6, 4],
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
# 6. SECCIÓN 3: RETOS, EVENTOS Y MENTORES
# ==========================================
col_r1, col_r2, col_r3 = st.columns(3)

with col_r1:
    st.subheader("🎯 Innovación Abierta y Retos")
    st.info("**Retos Territoriales Activos:**\n* Miraflores\n* Callao Tech")
    st.metric(label="Innovación Abierta EU (Participantes)", value=buscar_valor_flexible("eu", "1"))
    st.metric(label="Polinización (Participantes)", value=buscar_valor_flexible("polinización", "1"))

with col_r2:
    st.subheader("📅 Eventos Internacionales EULAC")
    datos_eventos = {
        'Sede / Evento': ['EULAC LIMA', 'EULAC CIX', 'EULAC AQP'],
        'Aforo Alcanzado': [
            str(buscar_valor_flexible("lim", "120")) + " Pax", 
            str(buscar_valor_flexible("cix", "120")) + " Pax", 
            str(buscar_valor_flexible("aqp", "120")) + " Pax"
        ]
    }
    st.table(pd.DataFrame(datos_eventos))

with col_r3:
    st.subheader("🧠 Capital Intelectual")
    st.metric(label="Red Global de Mentores", value=str(buscar_valor_flexible("mentores", "120")) + " Profesionales", delta="Estrategas")

st.markdown("---")

# ==========================================
# 7. SECCIÓN 4: ANALÍTICA DIGITAL Y REDES
# ==========================================
st.subheader("🌐 Visitas a Plataformas vs. Comunidad Digital")
col_v1, col_v2 = st.columns(2)

with col_v1:
    df_visitas = df[df['Categoria_Limpia'].str.contains("VISITA", na=False)].copy()
    
    if not df_visitas.empty and df_visitas['Valor_Numerico'].sum() > 0:
        df_visitas = df_visitas.dropna(subset=['Valor_Numerico']).sort_values(by='Valor_Numerico')
        fig_visitas = px.bar(df_visitas, x='Valor_Numerico', y='Item', orientation='h', template="plotly_white", color_discrete_sequence=['#0f172a'])
    else:
        # Valores de respaldo mapeados de forma segura
        items_v = ['ATIPAQ', 'Mentores', 'Miraflores', 'Pre-incubación', 'Incubación', 'Callao Tech']
        vals_v = [buscar_valor_flexible("atipaq", 243, True), buscar_valor_flexible("mentores", 114, True), buscar_valor_flexible("miraflores", 64, True), pre_inc, inc, buscar_valor_flexible("callao", 7, True)]
        df_v_mock = pd.DataFrame({'Item': items_v, 'Valor': vals_v}).sort_values(by='Valor')
        fig_visitas = px.bar(df_v_mock, x='Valor', y='Item', orientation='h', template="plotly_white", color_discrete_sequence=['#0f172a'])
        
    fig_visitas.update_layout(title='Volumen de Tráfico y Participación por Canal', plot_bgcolor='#ffffff', paper_bgcolor='#ffffff', height=400, font=dict(color="#000000"))
    fig_visitas.update_xaxes(title_text="Interacciones", tickfont=dict(color="#000000"), showgrid=True, gridcolor="#e2e8f0")
    fig_visitas.update_yaxes(title_text="Canal", tickfont=dict(color="#000000"))
    st.plotly_chart(fig_visitas, use_container_width=True)

with col_v2:
    # FILTRADO ROBUSTO INDIVIDUAL PARA REDES SOCIALES
    redes_lista = ['TikTok', 'Instagram', 'Facebook', 'LinkedIn', 'YouTube']
    valores_redes = [
        buscar_valor_flexible("tiktok", 3000, es_numerico=True),
        buscar_valor_flexible("instagram", 2000, es_numerico=True),
        buscar_valor_flexible("facebook", 2000, es_numerico=True),
        buscar_valor_flexible("linkedin", 1000, es_numerico=True),
        buscar_valor_flexible("youtube", 200, es_numerico=True)
    ]
    
    df_redes_lista = pd.DataFrame({
        'Red Social': redes_lista,
        'Miembros': valores_redes
    })
    
    fig_redes = px.bar(
        df_redes_lista,
        x='Red Social',
        y='Miembros',
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
