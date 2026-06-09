import streamlit as st
from google import genai
from google.genai import types
import plotly.express as px
import pandas as pd
import pdfplumber
from fpdf import FPDF
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

# 2. CLASE TÉCNICA PARA RENDERIZAR EL ACTA EN UN PDF FORMAL INSTITUCIONAL
class PDF_Acta(FPDF):
    def header(self):
        # Membrete institucional superior
        self.set_font('Arial', 'B', 10)
        self.set_text_color(100, 110, 120)
        self.cell(0, 10, 'MISION 3 - UNIVERSIDAD - COMITE DIRECTIVO SINTETICO', 0, 1, 'L')
        self.set_draw_color(180, 190, 200)
        self.line(10, 18, 200, 18)
        self.ln(10)

    def footer(self):
        # Pie de página con numeración y nota de confidencialidad
        self.set_y(-15)
        self.set_font('Arial', 'I', 8)
        self.set_text_color(150, 150, 150)
        self.cell(0, 10, 'Documento de Trazabilidad Agentica - Confidencial', 0, 0, 'L')
        self.cell(0, 10, f'Pagina {self.page_no()}', 0, 0, 'R')

def generar_pdf_descargable(contenido_acta):
    pdf = PDF_Acta()
    pdf.add_page()
    pdf.set_font("Arial", size=10)
    pdf.set_text_color(30, 30, 30)
    
    # Limpieza rigurosa de caracteres especiales para evitar corrupciones en FPDF (ISO-8859-1)
    clean_text = contenido_acta.encode('latin-1', 'replace').decode('latin-1')
    # Reemplazar formatos markdown comunes para una lectura limpia en el PDF
    clean_text = clean_text.replace("**", "").replace("#", "")
    
    pdf.multi_cell(0, 6, txt=clean_text)
    
    # SOLUCIÓN DEL LOG: Forzar la conversión del output a un bloque de bytes puro compatible con Streamlit
    pdf_output = pdf.output()
    if isinstance(pdf_output, str):
        return bytes(pdf_output, 'latin-1')
    else:
        return bytes(pdf_output)

# 3. FUNCIÓN PARA EXTRAER TEXTO DE LOS ARCHIVOS PDF ADJUNTOS (AGENT LAKE)
def extraer_texto_pdf(archivo_pdf):
    texto_completo = ""
    with pdfplumber.open(archivo_pdf) as pdf:
        for pagina in pdf.pages:
            texto_completo += pagina.extract_text() + "\n"
    return texto_completo

# 4. SECCIÓN LATERAL DE CONTROL (SIDEBAR)
st.sidebar.image("https://img.icons8.com/fluent/96/000000/artificial-intelligence.png", width=60)
st.sidebar.title("M3 Control Panel")
st.sidebar.markdown("---")

model_choice = st.sidebar.selectbox(
    "🤖 Motor de Inteligencia Principal", 
    ["gemini-2.5-flash", "gemini-2.5-pro"],
    help="Al usar tu cuenta prepago, el sistema responderá con alta velocidad y cuotas de peticiones ampliadas."
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

# 5. INTERFAZ GRÁFICA PRINCIPAL (HERO SECTION FUTURISTA)
st.image("https://images.unsplash.com/photo-1518770660439-4636190af475?auto=format&fit=crop&w=1200&q=80", use_container_width=True)

st.title("🧠 M3 Synthetic Board")
st.subheader("Plataforma Multiagente de Soporte a Decisiones Estratégicas")

# KPIs de Dashboard Corporativo en Pantalla
col_kpi1, col_kpi2, col_kpi3, col_kpi4 = st.columns(4)
col_kpi1.metric(label="Agentes Convocados", value="8 Expertos")
col_kpi2.metric(label="Estructura de Datos", value="Agent Lake V3")
col_kpi3.metric(label="Modo de Facturación", value="Credit Account (Active)")
col_kpi4.metric(label="Formatos de Salida", value="Markdown / PDF")

st.markdown("---")

# 6. FUENTE DE DATOS E INGESTIÓN DE ARCHIVOS (UX MEJORADO)
st.markdown("### 📂 Fuentes de Información del Comité")
col_input, col_file = st.columns([1, 1])

with col_input:
    caso_humano = st.text_area(
        "Instrucción u objetivo estratégico del Director Humano:",
        value="Evaluar si Misión 3 debe lanzar un reto de innovación abierta para mejorar la gestión de residuos en una municipalidad de Lima. Preparar recomendación, riesgos, aliados, campaña y plan operativo.",
        height=140
    )

with col_file:
    archivo_cargado = st.file_uploader(
        "Cargar documento anexo de soporte en PDF (Propuestas, bases de concursos, reportes técnicos):", 
        type=["pdf"]
    )
    if archivo_cargado:
        st.success("✅ Documento cargado exitosamente en el Agent Lake corporativo.")

# 7. PROMPT MAESTRO ESTRUCTURADO (Simula el debate jerárquico interno)
def construir_prompt_maestro(caso, contexto_pdf=""):
    contexto_extra = f"\n\n[CONTEXTO EXTENDIDO DEL DOCUMENTO INSTITUCIONAL ADJUNTO]:\n{contexto_pdf}" if contexto_pdf else ""
    return f"""
    Eres el sistema 'M3 Synthetic Board', una infraestructura multiagente jerárquica de Misión 3 de la universidad. 
    Tu objetivo es simular una deliberación completa de un comité directivo técnico sobre el siguiente caso y su documentación asociada.

    CASO A EVALUAR: "{caso}" {contexto_extra}

    Para resolver esto de forma integral, debes actuar simulando secuencialmente los siguientes 8 roles técnicos:
    1. ExpertoEcosistemas: Analiza impacto nacional/regional, gremios, universidades y alineación con la tercera misión universitaria.
    2. ExpertoInnovacion: Analiza novedad, diferenciación, TRL (madurez tecnológica) y riesgos científicos/técnicos.
    3. ExpertoEmprendimiento: Analiza viabilidad comercial, modelo de negocio y si requiere preincubación, incubación o aceleración.
    4. ExpertoVinculacion: Conecta la propuesta con facultades, investigadores, laboratorios y necesidades del mercado empresarial.
    5. ExpertoConcursos: Diseña criterios de evaluación, estructura de bases, embudos de selección y mitigación de sesgos regionales.
    6. ExpertoComunicaciones: Crea la narrativa estratégica, canales públicos (LinkedIn, prensa, mailing) y tono de la campaña.
    7. ExpertoAutomatizacion: Traduce la decisión en flujos digitales, formularios de captura, dashboards y tareas automatizadas.
    8. SecretarioGeneral: Analiza críticamente las opiniones de los 7 expertos anteriores, identifica fricciones y redacta el Acta Final.

    Por favor, genera una respuesta que contenga exactamente estas dos secciones principales separadas por los tags indicados:

    === SECCION_AUDITORIA ===
    Genera un resumen técnico estructurado de lo que dictamina CADA UNO de los 7 expertos especialistas de manera independiente. Usa viñetas claras y concisas para cada uno.

    === SECCION_ACTA ===
    Actúa como el Secretario General y redacta el documento formal institucional 'Acta del Comité Directivo Sintético M3' en formato Markdown con la siguiente estructura formal:
    # Acta Oficial del Comité Directivo Sintético M3
    - **Tema Evaluado**
    - **Agentes Participantes**
    - **Recomendaciones Clave Consolidadas**
    - **Consensos Detectados en el Comité**
    - **Disensos o Puntos de Fricción Técnica**
    - **Riesgos Críticos Identificados**
    - **Decisión Final Sugerida (Propuesta)**
    - **Plan de Acción Operativo (Paso a Paso de Implementación)**
    """

# 8. CONTROL DE EJECUCIÓN CON FEEDBACK VISUAL PREMIUM
if st.button("🚀 CONVOCAR COMITÉ Y EVALUAR FUENTES", use_container_width=True):
    if not api_key_final:
        st.error("❌ Acción bloqueada: No se detecta una clave API válida para conectar con los agentes.")
    else:
        try:
            client = genai.Client(api_key=api_key_final)
            
            # Extraer texto del PDF cargado en caso exista alguno
            texto_contexto_pdf = extraer_texto_pdf(archivo_cargado) if archivo_cargado else ""
            
            # Animaciones de la interfaz de usuario que muestran el progreso técnico en vivo
            with st.status("🛸 Sincronizando Agent Lake y ejecutando consultas en el comité virtual...", expanded=True) as status:
                
                if archivo_cargado:
                    st.write("📖 `[Data Ingestion]` Analizando y procesando las páginas del archivo PDF...")
                    time.sleep(1.0)
                
                st.write("🌐 `[Sesión]` Abriendo canales de comunicación segura con los 7 agentes especialistas...")
                time.sleep(1.2)
                
                st.write("🔬 `[Procesamiento]` Corriendo simulaciones cruzadas de impacto regional y TRL tecnológico...")
                time.sleep(1.2)
                
                st.write("✍️ `[Orquestación]` Secretario General consolidando dictamen final y abriendo acta institucional...")
                
                # EJECUCIÓN ULTRA EFICIENTE DE UNA SOLA LLAMADA MASIVA
                prompt_completo = construir_prompt_maestro(caso_humano, texto_contexto_pdf)
                response = client.models.generate_content(
                    model=model_choice,
                    contents=prompt_completo,
                    config=types.GenerateContentConfig(temperature=0.2)
                )
                
                resultado_raw = response.text
                status.update(label="⚡ Sesión concluida con éxito. Documentos listos.", state="complete", expanded=False)
            
            # PARSEO AUTOMÁTICO DE SECCIONES
            if "=== SECCION_ACTA ===" in resultado_raw:
                partes = resultado_raw.split("=== SECCION_ACTA ===")
                auditoria = partes[0].replace("=== SECCION_AUDITORIA ===", "").strip()
                acta = partes[1].strip()
            else:
                acta = resultado_raw
                auditoria = "Registro unificado en el cuerpo principal del documento."

            # Guardamos las respuestas en la memoria de estado de Streamlit
            st.session_state["acta_final_ok"] = acta
            st.session_state["lake_auditoria_ok"] = auditoria

        except Exception as e:
            st.error(f"Fallo en la comunicación agéntica de la API: {e}. Asegúrese de haber configurado de forma correcta su API Key.")

# 9. ENTREGA DE RESULTADOS EN ALTA FIDELIDAD (MÉTRICAS, PESTAÑAS Y EXPORTACIÓN PDF)
if "acta_final_ok" in st.session_state:
    st.markdown("### 🏆 Documentos de Salida del Comité")
    
    tab_acta, tab_trazabilidad, tab_graficos = st.tabs([
        "📜 Acta Ejecutiva Final", 
        "🔍 Auditoría de Agent Lake (Trazabilidad)", 
        "📊 Panel Analítico de Decisiones"
    ])
    
    with tab_acta:
        # Tarjeta visual contenedora con bordes definidos para el acta oficial
        with st.container(border=True):
            st.markdown(st.session_state["acta_final_ok"])
            
        # PROCESO DE COMPILACIÓN Y EMISIÓN EN PDF (BÚFER DE BYTES CORREGIDO)
        pdf_binario = generar_pdf_descargable(st.session_state["acta_final_ok"])
        
        st.download_button(
            label="📥 EMITIR Y DESCARGAR ACTA EN PDF",
            data=pdf_binario,
            file_name="Acta_Oficial_Comite_M3.pdf",
            mime="application/pdf",
            use_container_width=True
        )
        
    with tab_trazabilidad:
        st.info("La siguiente información es el registro técnico e independiente de lo que cada experto dictaminó en el Agent Lake antes de la consolidación del Secretario General.")
        with st.container(border=True):
            st.markdown(st.session_state["lake_auditoria_ok"])
            
    with tab_graficos:
        st.markdown("#### Simulación de Factibilidad del Comité Técnico")
        st.caption("Gráfico analítico interactivo generado con Plotly para la visualización del peso consultivo de cada departamento.")
        
        data_simulada = {
            "Agente Especialista": ["Ecosistemas", "Innovación", "Emprendimiento", "Vinculación", "Concursos", "Comunicaciones", "Automatización"],
            "Nivel de Impacto (%)": [85, 90, 75, 80, 95, 70, 85]
        }
        df = pd.DataFrame(data_simulada)
        fig = px.bar(df, x="Agente Especialista", y="Nivel de Impacto (%)", color="Nivel de Impacto (%)", title="Puntuación de Priorización de Variables Strategicas", template="plotly_dark")
        st.plotly_chart(fig, use_container_width=True)
