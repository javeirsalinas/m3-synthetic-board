import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import re
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

# BOTÓN EN LA BARRA LATERAL PARA BORRAR CACHÉ
if st.sidebar.button("🔄 Forzar Recarga (Limpiar Caché)"):
    st.cache_data.clear()
    st.success("¡Caché de Google Sheets limpiada!")

# ==========================================
# 2. CONEXIÓN EN TIEMPO REAL A GOOGLE SHEETS
# ==========================================
@st.cache_data(ttl="2s") 
def cargar_datos():
    conn = st.connection("gsheets", type=GSheetsConnection)
    url_directa = "https://docs.google.com/spreadsheets/d/1aEIyDmHuHxzei8IRqMFKYDIZ1Hc3lvQoU6odzyuiL9M/edit?usp=sharing"
    return conn.read(spreadsheet=url_directa, sheet="Hoja 1")

try:
    df = cargar_datos()
    # Limpieza estricta de nombres de columnas
    df.columns = df.columns.str.strip()
    
    # Todo a string para evitar errores por tipos mezclados
    df['Item_String'] = df['Item'].astype(str).str.strip().str.lower()
    df['Valor_String'] = df['Valor'].astype(str).str.strip()
except Exception as e:
    st.error("⚠️ Error al procesar la pestaña 'Hoja 1' de Google Sheets")
    st.stop()

# Funciones globales que extraen texto o limpian números dinámicamente
def extraer_valor_kpi(palabra, defecto):
    try:
        sub_df = df[df['Item_String'].str.contains(palabra.lower(), na=False)]
        if not sub_df.empty:
            return str(sub_df.iloc[0]['Valor_String'])
        return defecto
    except:
        return defecto

def extraer_numero_kpi(palabra, defecto):
    try:
        sub_df = df[df['Item_String'].str.contains(palabra.lower(), na=False)]
        if not sub_df.empty:
            val_raw = str(sub_df.iloc[0]['Valor_String'])
            # Filtramos solo los dígitos numéricos usando expresiones regulares
            solo_numeros = re.sub(r'[^\d]', '', val_raw)
            if solo_numeros:
                return int(solo_numeros)
        return defecto
    except:
        return defecto

# Muestra la tabla original arriba para auditoría visual directa
st.sidebar.markdown("### 📊 Vista previa de los datos leídos:")
st.sidebar.dataframe(df[['Categoria', 'Item', 'Valor']])

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
    st.metric(label="Comité Plataforma", value=extraer_valor_kpi("comite", "Funcionando"), delta="✓ Estado")
with col_p2:
    st.metric(label="Dashboard Plataforma", value=extraer_valor_kpi("dashboard", "Proceso"), delta="✓ Estado")
with col_p3:
    st.metric(label="Calculadora Valor", value=extraer_valor_kpi("calculadora", "Funcionando"), delta="✓ Estado")
with col_p4:
    st.metric(label="Consultoría Innovación", value=extraer_valor_kpi("consultoria", "Proceso"), delta="✓ Estado")
with col_p5:
    st.metric(label="Curso E&I Transversal", value=extraer_valor_kpi("curso", "Proceso"), delta="✓ Estado")

st.markdown("---")

# ==========================================
# 5. SECCIÓN 2: PIPELINE DE EMPRENDIMIENTO Y VINCULACIÓN
# ==========================================
col_izq, col_der = st.columns([1.2, 1])

with col_izq:
    st.subheader("🚀 Embudo del Emprendedor (E&I)")
    
    pre_inc = extraer_numero_kpi("preincubacion", 60)
    inc = extraer_numero_kpi("incubacion", 25)
    aceleracion = extraer_numero_kpi("aceleracion", 0)

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
    
    u = extraer_numero_kpi("universidades", 30)
    i = extraer_numero_kpi("incubadoras", 20)
    c = extraer_numero_kpi("camaras", 20)
    a = extraer_numero_kpi("asociaciones", 6)
    ins = extraer_numero_kpi("instituciones", 4)
    
    df_ve_dinamico = pd.DataFrame({
        'Entidad': ['Universidades', 'Incubadoras', 'Cámaras', 'Asociaciones', 'Instituciones'],
        'Cantidad': [u, i, c, a, ins]
    })
    
    fig_pie = px.pie(
        df_ve_dinamico, 
        values='Cantidad', 
        names='Entidad',
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
    st.info(f"**Retos Territoriales Activos:**\n* {extraer_valor_kpi('innovacion abierta', 'Miraflores')}")
    st.metric(label="Polinización (Participantes)", value=extraer_numero_kpi("polinización", 1))

with col_r2:
    st.subheader("📅 Eventos Internacionales EULAC")
    datos_eventos = {
        'Sede / Evento': ['EULAC LIMA', 'EULAC CIX', 'EULAC AQP', 'Mentores'],
        'Aforo Alcanzado': [
            extraer_valor_kpi("eulac lim", "120 Pax"), 
            extraer_valor_kpi("eulac cix", "120 Pax"), 
            extraer_valor_kpi("eulac aqp", "120 Pax"),
            extraer_valor_kpi("mentores", "120 Pax")
        ]
    }
    st.table(pd.DataFrame(datos_eventos))

with col_r3:
    st.subheader("🧠 Viajes e Impacto")
    st.metric(label="Visitas Campus", value=extraer_numero_kpi("visitas campus", 12))

st.markdown("---")

# ==========================================
# 7. SECCIÓN 4: ANALÍTICA DIGITAL (EXTRACCIÓN POR FILTRADO DE TEXTO)
# ==========================================
st.subheader("🌐 Visitas a Plataformas vs. Comunidad Digital")
col_v1, col_v2 = st.columns(2)

with col_v1:
    items_v = ['ATIPAQ', 'Miraflores', 'Mentores', 'Callao Tech']
    vals_v = [
        extraer_numero_kpi("atipaq", 268), 
        extraer_numero_kpi("miraflores", 64), 
        extraer_numero_kpi("mentores", 113),
        extraer_numero_kpi("callao tech", 8)
    ]
    df_visitas_dinamico = pd.DataFrame({'Item': items_v, 'Valor': vals_v}).sort_values(by='Valor')
    
    fig_visitas = px.bar(df_visitas_dinamico, x='Valor', y='Item', orientation='h', template="plotly_white", color_discrete_sequence=['#0f172a'])
    fig_visitas.update_layout(title='Volumen de Tráfico por Canal', plot_bgcolor='#ffffff', paper_bgcolor='#ffffff', height=380, font=dict(color="#000000"))
    fig_visitas.update_xaxes(title_text="Interacciones", tickfont=dict(color="#000000"), showgrid=True, gridcolor="#e2e8f0")
    fig_visitas.update_yaxes(title_text="Canal", tickfont=dict(color="#000000"))
    st.plotly_chart(fig_visitas, use_container_width=True)

with col_v2:
    # Extracción individual buscando la palabra clave dentro de tu columna 'Item'
    redes_lista = ['TikTok', 'Instagram', 'LinkedIn', 'Facebook', 'YouTube']
    valores_redes = [
        extraer_numero_kpi("tiktok", 7211),
        extraer_numero_kpi("instagram", 2146),
        extraer_numero_kpi("linkedin", 829),
        extraer_numero_kpi("facebook", 386),
        extraer_numero_kpi("youtube", 53)
    ]
    
    df_redes_reales = pd.DataFrame({
        'Red Social': redes_lista,
        'Miembros': valores_redes
    }).sort_values(by='Miembros', ascending=False)
    
    fig_redes = px.bar(
        df_redes_reales,
        x='Red Social',
        y='Miembros',
        title='Seguidores Totales en Canales Digitales (Actualizado)',
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
    "Sincronizado correctamente con la pestaña 'Hoja 1' del Google Sheet."
    "</center>", 
    unsafe_allow_html=True
)
