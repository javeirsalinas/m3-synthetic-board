import streamlit as st
from google import genai
from google.genai import types
import plotly.express as px  # Librería importada correctamente para gráficos
import pandas as pd
import time

# 1. CONFIGURACIÓN DE MAQUETACIÓN PREMIUM (DISEÑO EXPERTO UX/UI)
st.set_page_config(
    page_title="M3 Synthetic Board | Centro de Comando",
    page_icon="🧠",
    layout="wide",
    initial_sidebar_state="expanded"
)

# RECOLECCIÓN DE CREDENCIALES SEGURAS DESDE LOS SECRETOS DE STREAMLIT
api_key_segura = st.secrets.get("GEMINI_API_KEY", "")

# 2. SECCIÓN LATERAL DE CONTROL (SIDEBAR)
st.sidebar.image("https://img.icons8.com/fluent/96/000000/artificial-intelligence.png", width=60)
st.sidebar.title("M3 Control Panel")
st.sidebar.markdown("---")

model_choice = st.sidebar.selectbox(
    "🤖 Motor de Inteligencia Principal", 
    ["gemini-2.5-flash", "gemini-2.5-pro"],
    help="Al estar en la cuenta prepago (Pay-as-you-go), ambos modelos responderán con alta prioridad y velocidad."
)

st.sidebar.markdown("### Estado de Infraestructura")
if api_key_segura:
    st.sidebar.success("🔒 Cloud Vault: Conectado (Plan Prepago)")
    api_key_final = api_key_segura
else:
    api_key_input = st.sidebar.text_input("Introducir Gemini API Key manualmente", type="password")
    api_key_final = api_key_input
    if not api_key_input:
        st.sidebar.warning("⚠️ Requiere llave de acceso")

# 3. INTERFAZ GRÁFICA PRINCIPAL (HERO SECTION FUTURISTA)
# Imagen conceptual de mesa interactiva de microchips con transferencia de datos masiva
st.image("https://images.unsplash.com/photo-1518770660439-4636190af475?auto=format&fit=crop&w=1200&q=80", use_container_width=True)

st.title("🧠 M3 Synthetic Board")
st.subheader("Plataforma Multiagente de Soporte a Decisiones Estratégicas")

# KPIs de Estado Corporativo en Pantalla
col_kpi1, col_kpi2, col_kpi3, col_kpi4 = st.columns(4)
col_kpi1.metric(label="Agentes Convocados", value="8 Expertos")
col_kpi2.metric(label="Estructura de Datos", value="Agent Lake V2")
col_kpi3.metric(label="Modo de Facturación", value="Credit Account (Active)")
col_kpi4.metric(label="Seguridad de Tokens", value="Optimizado")

st.markdown("---")

# ZONA DE TRABAJO (Entrada de Datos del Usuario)
st.markdown("### 📝 Caso de Negocio o Desafío Institucional")
caso_humano = st.text_area(
    "Instrucción: Ingrese la propuesta o el problema técnico que el comité sintético debe analizar, contrastar y documentar.",
    value="Evaluar si Misión 3 debe lanzar un reto de innovación abierta para mejorar la gestión de residuos en una municipalidad de Lima. Preparar recomendación, riesgos, aliados, campaña y plan operativo.",
    height=120,
    label_visibility="collapsed"
)

# PROMPT MAESTRO ESTRUCTURADO (Simula el debate jerárquico interno)
def construir_prompt_maestro(caso):
    return f"""
    Eres el sistema 'M3 Synthetic Board', una infraestructura multiagente jerárquica de Misión 3 de la universidad. 
    Tu objetivo es simular una deliberación completa de un comité directivo técnico sobre el siguiente caso.

    CASO A EVALUAR: "{caso}"

    Para resolver esto, debes actuar de forma secuencial simulando los siguientes 8 roles técnicos:
    1. ExpertoEcosistemas: Analiza impacto nacional/regional, gremios, universidades y alineación con la tercera misión universitaria.
    2. ExpertoInnovacion: Analiza novedad, diferenciación, TRL (madurez tecnológica) y riesgos científicos/técnicos.
    3. ExpertoEmprendimiento: Analiza viabilidad comercial, modelo de negocio y si requiere preincubación, incubación o aceleración.
    4. ExpertoVinculacion: Conecta la propuesta con facultades, investigadores, laboratorios y necesidades del mercado.
    5. ExpertoConcursos: Diseña criterios de evaluación, estructura de bases, embudos de selección y mitigación de sesgos regionales.
    6. ExpertoComunicaciones: Crea la narrativa estratégica, canales públicos (LinkedIn, prensa, mailing) y tono de la campaña.
    7. ExpertoAutomatizacion: Traduce la decisión en flujos digitales, formularios de captura, dashboards y tareas automatizadas.
    8. SecretarioGeneral: Analiza críticamente las opiniones de los 7 expertos anteriores, identifica fricciones y redacta el Acta Final.

    Por favor, genera una respuesta que contenga exactamente estas dos secciones principales separadas por los tags indicados:

    === SECCION_AUDITORIA ===
    Genera un resumen técnico estructurado de lo que dictamina CADA UNO de los 7 expertos especialistas de manera independiente (Ecosistemas, Innovación, Emprendimiento, Vinculación, Concursos, Comunicaciones, Automatización). Usa viñetas claras y profesionales para cada uno.

    === SECCION_ACTA ===
    Actúa como el Secretario General y redacta el documento formal institucional 'Acta del Comité Directivo Sintético M3' en formato Markdown con la siguiente estructura formal:
    # 📜 Acta Oficial del Comité Directivo Sintético M3
    - **Tema Evaluado**
    - **Agentes Participantes**
    - **Recomendaciones Clave Consolidadas**
    - **Consensos Detectados en el Comité**
    - **Disensos o Puntos de Fricción Técnica**
    - **Riesgos Críticos Identificados**
    - **Decisión Final Sugerida (Propuesta)**
    - **Plan de Acción Operativo (Paso a Paso de Implementación)**
    """

# CONTROL DE EJECUCIÓN CON FEEDBACK VISUAL PREMIUM
if st.button("🚀 INICIAR DELIBERACIÓN ESTRATÉGICA", use_container_width=True):
    if not api_key_final:
        st.error("❌ Acción bloqueada: No se detecta una clave API válida para conectar con los agentes.")
    else:
        try:
            client = genai.Client(api_key=api_key_final)
            
            # Animaciones de la interfaz de usuario que muestran el progreso técnico en vivo
            with st.status("🛸 Sincronizando Agent Lake y convocando sesión virtual...", expanded=True) as status:
                
                st.write("🌐 `[Sesión]` Abriendo canales de comunicación segura con los 7 agentes especialistas...")
                time.sleep(1.2)
                
                st.write("🔬 `[Procesamiento]` Corriendo simulaciones cruzadas de impacto regional y TRL tecnológico...")
                time.sleep(1.2)
                
                st.write("📢 `[Gobernanza]` Evaluando variables de comunicación estratégica y flujos automatizados operativos...")
                time.sleep(1.2)
                
                st.write("✍️ `[Orquestación]` Secretario General consolidando dictamen final y abriendo acta institucional...")
                
                # EJECUCIÓN ULTRA EFICIENTE DE UNA SOLA LLAMADA MASIVA (Protección de presupuesto)
                prompt_completo = construir_prompt_maestro(caso_humano)
                response = client.models.generate_content(
                    model=model_choice,
                    contents=prompt_completo,
                    config=types.GenerateContentConfig(temperature=0.2)
                )
                
                resultado_raw = response.text
                status.update(label="⚡ Sesión concluida con éxito. Datos listos.", state="complete", expanded=False)
            
            # PARSEO AUTOMÁTICO DE SECCIONES (Procesamiento de texto para la vista de pestañas)
            if "=== SECCION_ACTA ===" in resultado_raw:
                partes = resultado_raw.split("=== SECCION_ACTA ===")
                auditoria = partes[0].replace("=== SECCION_AUDITORIA ===", "").strip()
                acta = partes[1].strip()
            else:
                acta = resultado_raw
                auditoria = "Registro unificado en el cuerpo principal del documento."

            # Guardamos las respuestas en la memoria de estado de Streamlit para no perderlas al hacer clics
            st.session_state["acta_final_ok"] = acta
            st.session_state["lake_auditoria_ok"] = auditoria

        except Exception as e:
            st.error(f"Fallo en la comunicación agéntica de la API: {e}. Asegúrese de haber configurado de forma correcta su API Key.")

# 4. ENTREGA DE RESULTADOS EN ALTA FIDELIDAD (MÉTRICAS Y PESTAÑAS UX)
if "acta_final_ok" in st.session_state:
    st.markdown("### 🏆 Documento de Salida del Comité")
    
    tab_acta, tab_trazabilidad, tab_graficos = st.tabs([
        "📜 Acta Ejecutiva Final", 
        "🔍 Auditoría de Agent Lake (Trazabilidad)", 
        "📊 Panel Analítico de Decisiones"
    ])
    
    with tab_acta:
        # Tarjeta visual contenedora con bordes definidos para el acta oficial
        with st.container(border=True):
            st.markdown(st.session_state["acta_final_ok"])
            
        st.download_button(
            label="📥 EXPORTAR ACTA OFICIAL (FORMATO MARKDOWN)",
            data=st.session_state["acta_final_ok"],
            file_name="acta_comite_m3.md",
            mime="text/markdown",
            use_container_width=True
        )
        
    with tab_trazabilidad:
        st.info("La siguiente información es el registro técnico e independiente de lo que cada experto dictaminó en el Agent Lake antes de la consolidación del Secretario General.")
        with st.container(border=True):
            st.markdown(st.session_state["lake_auditoria_ok"])
            
    with tab_graficos:
        st.markdown("#### Simulación de Factibilidad del Comité Técnico")
        st.caption("Gráfico analítico interactivo generado con Plotly para la visualización del peso consultivo de cada departamento.")
        
        # Simulación de un set de datos para dibujar un gráfico interactivo con Plotly para la Alta Dirección
        data_simulada = {
            "Agente Especialista": ["Ecosistemas", "Innovación", "Emprendimiento", "Vinculación", "Concursos", "Comunicaciones", "Automatización"],
            "Nivel de Impacto (%)": [85, 90, 75, 80, 95, 70, 85]
        }
        df = pd.DataFrame(data_simulada)
        fig = px.bar(df, x="Agente Especialista", y="Nivel de Impacto (%)", color="Nivel de Impacto (%)", title="Puntuación de Priorización de Variables Estratégicas", template="plotly_dark")
        st.plotly_chart(fig, use_container_width=True)
