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

# ==========================================
# 2. CONEXIÓN EN TIEMPO REAL A GOOGLE SHEETS
# ==========================================
@st.cache_data(ttl="5s") # Actualización rápida en 5 segundos
def cargar_datos():
    conn = st.connection("gsheets", type=GSheetsConnection)
    url_directa = "https://docs.google.com/spreadsheets/d/1aEIyDmHuHxzei8IRqMFKYDIZ1Hc3lvQoU6odzyuiL9M/edit?usp=sharing"
    return conn.read(spreadsheet=url_directa)

try:
    df = cargar_datos()
    df.columns = df.columns.str.strip()
    # Limpieza base para textos generales
    df['item_minuscula'] = df['Item'].astype(str).str.strip().str.lower()
except Exception as e:
    st.error("⚠️ Error al procesar la estructura de Google Sheets")
    st.stop()

# NUEVO MOTOR REGEX: Extrae los dígitos numéricos de celdas como "miembrosLinkedin829"
def extraer_numero_de_texto(palabra_clave, valor_defecto):
    try:
        # Buscamos la fila que contiene la palabra clave (ej: 'linkedin')
        filtro = df[df['item_minuscula'].str.contains(palabra_clave.lower(), na=False)]
        if not filtro.empty:
            texto_celda = str(filtro.iloc[0]['Item'])
            # Expresión regular para extraer todos los números continuos del texto
            numeros_encontrados = re.findall(r'\d+', texto_celda)
            if numeros_encontrados:
                return int(numeros_encontrados[0])
            
            # Si no hay números en Item, intentamos leer la columna Valor por si acaso
            val_col = pd.to_numeric(filtro.iloc[0]['Valor'], errors='coerce')
            if not pd.isna(val_col):
                return int(val_col)
        return valor_defecto
    except:
        return valor_defecto

def buscar_texto_por_palabra(palabra, valor_defecto):
    try:
        filtro = df[df['item_minuscula'].str.contains(palabra.lower(), na=False)]
        if not filtro.empty:
            # Si la columna Valor está vacía, mostramos el texto de la columna Item limpia
            val_col = str(filtro.iloc[0]['Valor']).strip()
            if val_col and val_col != "nan":
                return val_col
            return str(filtro.iloc[0]['Item'])
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
# 4. SECCIÓN 1: ESTADO OPERATIVO DE PLATAFORMAS
# ==========================================
st.subheader("🏢 Estado de la Unidad y Plataformas")
col_p1, col_p2, col_p3, col_p4, col_p5 = st.columns(5)

with col_p1:
    st.metric(label="Comité Plataforma", value=buscar_texto_por_palabra("comité", "Funcionando"), delta="✓ Estado")
with col_p2:
    st.metric(label="Dashboard Plataforma", value=buscar_texto_por_palabra("dashboard", "Funcionando"), delta="✓ Estado")
with col_p3:
    st.metric(label="Calculadora Valor", value=buscar_texto_por_palabra("calculadora", "Funcionando"), delta="✓ Estado")
with col_p4:
    st.metric(label="Consultoría Innovación", value=buscar_texto_por_palabra("consultoría", "Proyecto"), delta="✓ Estado")
with col_p5:
    st.metric(label="Curso E&I Transversal", value=buscar_texto_por_palabra("curso", "Proyecto"), delta="✓ Estado")

st.markdown("---")

# ==========================================
# 5. SECCIÓN 2: PIPELINE DE EMPRENDIMIENTO Y VINCULACIÓN
# ==========================================
col_izq, col_der = st.columns([1.2, 1])

with col_izq:
    st.subheader("🚀 Embudo del Emprendedor (E&I)")
    
    pre_inc = extraer_numero_de_texto("pre", 60)
    inc = extraer_numero_de_texto("incubación", 25)
    aceleracion = extraer_numero_de_texto("aceleración", 0)

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
    
    u = extraer_numero_de_texto("universidades", 20)
    i = extraer_numero_de_texto("incubadoras", 20)
    c = extraer_numero_de_texto("cámaras", 19)
    a = extraer_numero_de_texto("asociaciones", 6)
    ins = extraer_numero_de_texto("instituciones", 4)
    
    df_ve_dinamico = pd.DataFrame({
        'Item': ['Universidades', 'Incubadoras', 'Cámaras', 'Asociaciones', 'Instituciones'],
        'Valor': [u, i, c, a, ins]
    })
    
    fig_pie = px.pie(
        df_ve_dinamico, 
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
# 6. SECCIÓN 3: RETOS, EVENTOS Y MENTORES
# ==========================================
col_r1, col_r2, col_r3 = st.columns(3)

with col_r1:
    st.subheader("🎯 Innovación Abierta y Retos")
    st.info("**Retos Territoriales Activos:**\n* Miraflores\n* Callao Tech")
    st.metric(label="Innovación Abierta EU (Participantes)", value=extraer_numero_de_texto("eu", 1))
    st.metric(label="Polinización (Participantes)", value=extraer_numero_de_texto("polinización", 1))

with col_r2:
    st.subheader("📅 Eventos Internacionales EULAC")
    datos_eventos = {
        'Sede / Evento': ['EULAC LIMA', 'EULAC CIX', 'EULAC AQP'],
        'Aforo Alcanzado': [
            str(extraer_numero_de_texto("lim", 120)) + " Pax", 
            str(extraer_numero_de_texto("cix", 120)) + " Pax", 
            str(extraer_numero_de_texto("aqp", 120)) + " Pax"
        ]
    }
    st.table(pd.DataFrame(datos_eventos))

with col_r3:
    st.subheader("🧠 Capital Intelectual")
    st.metric(label="Red Global de Mentores", value=str(extraer_numero_de_texto("mentores", 120)) + " Profesionales", delta="Estrategas")

st.markdown("---")

# ==========================================
# 7. SECCIÓN 4: ANALÍTICA DIGITAL Y REDES (EXTRACCIÓN INTELIGENTE)
# ==========================================
st.subheader("🌐 Visitas a Plataformas vs. Comunidad Digital")
col_v1, col_v2 = st.columns(2)

with col_v1:
    items_v = ['ATIPAQ', 'Mentores', 'Miraflores', 'Pre-incubación', 'Incubación', 'Callao Tech']
    vals_v = [
        extraer_numero_de_texto("atipaq", 243), 
        extraer_numero_de_texto("mentores", 114), 
        extraer_numero_de_texto("miraflores", 64), 
        pre_inc, 
        inc, 
        extraer_numero_de_texto("callao", 7)
    ]
    df_v_mock = pd.DataFrame({'Item': items_v, 'Valor': vals_v}).sort_values(by='Valor')
    fig_visitas = px.bar(df_v_mock, x='Valor', y='Item', orientation='h', template="plotly_white", color_discrete_sequence=['#0f172a'])
        
    fig_visitas.update_layout(title='Volumen de Tráfico y Participación por Canal', plot_bgcolor='#ffffff', paper_bgcolor='#ffffff', height=400, font=dict(color="#000000"))
    fig_visitas.update_xaxes(title_text="Interacciones", tickfont=dict(color="#000000"), showgrid=True, gridcolor="#e2e8f0")
    fig_visitas.update_yaxes(title_text="Canal", tickfont=dict(color="#000000"))
    st.plotly_chart(fig_visitas, use_container_width=True)

with col_v2:
    # PROCESAMIENTO CON EXTRACCIÓN AUTOMÁTICA DE DÍGITOS
    redes_lista = ['TikTok', 'Instagram', 'Facebook', 'LinkedIn', 'YouTube']
    valores_redes = [
        extraer_numero_de_texto("tiktok", 7211),
        extraer_numero_de_texto("instagram", 2146),
        extraer_numero_de_texto("facebook", 386),
        extraer_numero_de_texto("linkedin", 829),
        extraer_numero_de_texto("youtube", 53)
    ]
    
    df_redes_lista = pd.DataFrame({
        'Red Social': redes_lista,
        'Miembros': valores_redes
    }).sort_values(by='Miembros', ascending=False)
    
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
