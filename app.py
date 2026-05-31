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

# Inyección de CSS para diseño claro corporativo y letras negras de alto contraste
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
    h1 { color: #000000 !important; font-family: 'Helvetica Neue', Arial, sans-serif; font-weight: 700; }
    h2, h3 { color: #0f172a !important; font-family: Arial, sans-serif; font-weight: 600; }
    p, span, li, td, th { color: #000000 !important; }
    .stTable { background-color: #ffffff !important; }
    </style>
    """, unsafe_allow_html=True)

# BOTÓN EN LA BARRA LATERAL PARA CONTROL DE ACTUALIZACIONES
if st.sidebar.button("🔄 Forzar Recarga (Limpiar Caché)"):
    st.cache_data.clear()
    st.success("¡Caché de Google Sheets limpiada exitosamente!")

# ==========================================
# 2. CONEXIÓN EN TIEMPO REAL A TU RECLASIFICACIÓN
# ==========================================
url_directa = "https://docs.google.com/spreadsheets/d/1aEIyDmHuHxzei8IRqMFKYDIZ1Hc3lvQoU6odzyuiL9M/edit?usp=sharing"

@st.cache_data(ttl="2s") # Tiempo de respuesta ultra rápido
def cargar_pestana(nombre_pestana):
    conn = st.connection("gsheets", type=GSheetsConnection)
    return conn.read(spreadsheet=url_directa, sheet=nombre_pestana)

try:
    # Carga de las 3 pestañas nuevas detectadas en tus capturas
    df_plataformas = cargar_pestana("Plataformas")
    df_gestion = cargar_pestana("Gestion_EI")
    df_eventos = cargar_pestana("Eventos_EULAC")
    
    # Limpieza estándar de textos y nombres de columnas
    df_plataformas.columns = df_plataformas.columns.str.strip()
    df_gestion.columns = df_gestion.columns.str.strip()
    df_eventos.columns = df_eventos.columns.str.strip()
    
    # Estandarizamos a minúsculas la columna de categorías de tu pestaña Gestion_EI
    df_gestion['Categoria'] = df_gestion['Categoria'].astype(str).str.strip().str.lower()
    df_gestion['Item_Limpio'] = df_gestion['Item'].astype(str).str.strip().str.lower()
    df_gestion['Valor_Num'] = pd.to_numeric(df_gestion['Valor'], errors='coerce')
except Exception as e:
    st.error("⚠️ Error al conectar con la estructura de las nuevas pestañas")
    st.stop()

# ==========================================
# 3. CABECERA EJECUTIVA INSTITUCIONAL
# ==========================================
st.title("🏛️ Centro de Emprendimiento e Innovación - Misión 3")
st.markdown("### **Dashboard de Indicadores Estratégicos y de Gestión**")
st.markdown("**Sincronización Multi-Pestaña Automatizada en Tiempo Real**")
st.markdown("---")

# ==========================================
# 4. SECCIÓN 1: ESTADO OPERATIVO DE PLATAFORMAS
# ==========================================
st.subheader("🏢 Estado de la Unidad y Plataformas")
cols_plat = st.columns(len(df_plataformas))

for index, row in df_plataformas.iterrows():
    with cols_plat[index % len(df_plataformas)]:
        st.metric(label=str(row['Plataforma']), value=str(row['Estado']), delta="✓ Monitoreo")

st.markdown("---")

# ==========================================
# 5. SECCIÓN 2: PIPELINE DE EMPRENDIMIENTO Y VINCULACIÓN
# ==========================================
col_izq, col_der = st.columns([1.2, 1])

with col_izq:
    st.subheader("🚀 Embudo del Emprendedor (E&I)")
    
    # Filtramos las fases de tu categoría 'programa'
    df_embudo = df_gestion[df_gestion['Categoria'] == 'programa'].copy()
    # Excluimos IdealLab y Polinización del gráfico de embudo para mantener solo la línea base
    df_funnel_data = df_embudo[df_embudo['Item_Limpio'].isin(['preincubacion', 'incubacion', 'aceleracion'])].copy()
    
    # Estética visual: Capitalizamos los textos antes de graficar (ej: de 'incubacion' a 'Incubacion')
    df_funnel_data['Item_Display'] = df_funnel_data['Item'].astype(str).str.capitalize()

    fig_embudo = go.Figure(go.Funnel(
        y=df_funnel_data['Item_Display'],
        x=df_funnel_data['Valor_Num'],
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
    
    # Muestra automática de tus datos de la categoría entidades si existieran en el futuro
    df_entidades = df_gestion[df_gestion['Categoria'] == 'entidades'].copy()
    
    if not df_entidades.empty:
        fig_pie = px.pie(df_entidades, values='Valor_Num', names='Item', template="plotly_white", color_discrete_sequence=['#0f172a', '#1e293b', '#475569', '#94a3b8'])
    else:
        # Respaldo dinámico usando los datos fijos estructurados
        fig_pie = px.pie(
            names=['Cámaras', 'Universidades', 'Asociaciones', 'Instituciones'],
            values=[20, 30, 6, 4],
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
col_r1, col_r2 = st.columns([1, 2])

with col_r1:
    st.subheader("🎯 Innovación Abierta")
    st.info("**Retos Territoriales Activos:**\n* Miraflores\n* Callao Tech")
    
    # Buscamos de forma automatizada la fila de polinización en tu hoja Gestion_EI
    df_pol = df_gestion[df_gestion['Item_Limpio'] == 'polinización']
    val_pol = int(df_pol.iloc[0]['Valor_Num']) if not df_pol.empty and not pd.isna(df_pol.iloc[0]['Valor_Num']) else 1
    st.metric(label="Polinización (Participantes)", value=val_pol)

with col_r2:
    st.subheader("📅 Eventos Internacionales EULAC")
    # Mapeo directo y limpio de tu pestaña 3 de Eventos
    st.table(df_eventos)

st.markdown("---")

# ==========================================
# 7. SECCIÓN 4: ANALÍTICA DIGITAL Y REDES (ENLACE DIRECTO A TU PESTAÑA)
# ==========================================
st.subheader("🌐 Visitas a Plataformas vs. Comunidad Digital")
col_v1, col_v2 = st.columns(2)

with col_v1:
    # Extraemos las filas asignadas a la categoría 'trafico' en tu Excel
    df_visitas = df_gestion[df_gestion['Categoria'] == 'trafico'].copy().sort_values(by='Valor_Num')
    
    fig_visitas = px.bar(
        df_visitas, 
        x='Valor_Num', 
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
    # FILTRADO DIRECTO PARA LA CATEGORÍA 'redes' DESDE TU EXCEL REAL
    df_redes = df_gestion[df_gestion['Categoria'] == 'redes'].copy()
    
    # Capitalizamos los nombres para que en la gráfica aparezcan estéticos (ej: de 'linkedin' a 'Linkedin')
    df_redes['Red Social'] = df_redes['Item'].astype(str).str.capitalize()
    df_redes = df_redes.sort_values(by='Valor_Num', ascending=False)
    
    fig_redes = px.bar(
        df_redes,
        x='Red Social',
        y='Valor_Num',
        title='Seguidores Totales en Canales Digitales (Datos en Vivo)',
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
    "Infraestructura Cloud integrada mediante arquitectura relacional de múltiples pestañas."
    "</center>", 
    unsafe_allow_html=True
)
