import streamlit as st
from google import genai
from google.genai import types
import time

# 1. CONFIGURACIÓN DE MAQUETACIÓN PREMIUM
st.set_page_config(
    page_title="M3 Synthetic Board | Centro de Comando",
    page_icon="🧠",
    layout="wide",
    initial_sidebar_state="expanded"
)

# RECOLECCIÓN DE CREDENCIALES SEGURAS
api_key_segura = st.secrets.get("GEMINI_API_KEY", "")

# SYSTEM PROMPTS OPTIMIZADOS EN TOKENS (Respuestas Ultra-Ejecutivas)
RESTRICTION = " IMPORTANTE: Tu respuesta debe ser ultra-ejecutiva, directa al grano y tener un máximo de 150 palabras. Usa viñetas breves. No uses introducciones ni saludos."

SYSTEM_PROMPTS = {
    "SecretarioGeneral": (
        "Actúas como Secretario Técnico del Comité Directivo de Misión 3. Organiza la deliberación "
        "entre agentes expertos, identifica consensos y disensos, y prepara una recomendación ejecutiva "
        "estructurada en Markdown para validación humana final. Sé conciso y estratégico."
    ),
    "ExpertoEcosistemas": (
        "Actúas como el Experto en Ecosistemas de Misión 3. Evalúas el contexto nacional, regional, "
        "sectorial e institucional. ¿Qué impacto tendría en el ecosistema? ¿Qué actores deben participar? "
        "¿Cómo se alinea con la tercera misión universitaria?" + RESTRICTION
    ),
    "ExpertoEmprendimiento": (
        "Actúas como el Experto en Emprendimiento de Misión 3. Evalúas calidad de propuestas, "
        "modelos de negocio, tracción y escalabilidad. ¿El problema es real? ¿Es coherente el modelo? "
        "¿Qué programa corresponde: preincubación, incubación o aceleración?" + RESTRICTION
    ),
    "ExpertoInnovacion": (
        "Actúas como el Experto en Innovación de Misión 3. Evalúas novedad, diferenciación, madurez tecnológica "
        "y potencial de transferencia. ¿Es innovación incremental, sustancial o disruptiva? ¿Tiene base científica? "
        "¿Nivel de madurez y riesgos técnicos?" + RESTRICTION
    ),
    "ExpertoVinculacion": (
        "Actúas como el Experto en Vinculación Universidad-Empresa de Misión 3. Conecta oferta académica, "
        "investigación, empresas y retos. ¿Qué facultades/laboratorios participan? ¿Qué empresas se benefician? "
        "¿Cómo convertir conocimiento académico en valor?" + RESTRICTION
    ),
    "ExpertoConcursos": (
        "Actúas como el Experto en Concursos y Programas de Misión 3. Diseña bases, criterios, cronogramas, "
        "jurados y seguimiento. ¿Cómo mejorar las bases? ¿Qué criterios usar? ¿Cómo evitar sesgos regionales?" + RESTRICTION
    ),
    "ExpertoComunicaciones": (
        "Actúas como el Experto en Comunicaciones de Misión 3. Convierte la decisión en narrativa, campaña, "
        "LinkedIn, notas de prensa y mensajes institucionales. ¿Cuál es el mensaje estratégico? ¿Qué tono usar?" + RESTRICTION
    ),
    "ExpertoAutomatizacion": (
        "Actúas como el Experto en Automatización de Procesos de Misión 3. Traduce la decisión en flujos, "
        "formularios, dashboards, integraciones y tareas. ¿Qué se puede automatizar? ¿Qué herramientas usar?" + RESTRICTION
    )
}

# 2. SECCIÓN LATERAL DE CONTROL (SIDEBAR)
st.sidebar.image("https://img.icons8.com/fluent/96/000000/artificial-intelligence.png", width=60)
st.sidebar.title("M3 Control Panel")
st.sidebar.markdown("---")

model_choice = st.sidebar.selectbox(
    "🤖 Motor de Inteligencia Principal", 
    ["gemini-2.5-flash", "gemini-2.5-pro"],
    help="Gemini 2.5 Flash es altamente recomendado para evitar límites de cuota (Rate Limits)."
)

st.sidebar.markdown("### Estado de Infraestructura")
if api_key_segura:
    st.sidebar.success("🔒 Cloud Vault: Conectado")
    api_key_final = api_key_segura
else:
    api_key_input = st.sidebar.text_input("Introducir Gemini API Key manualmente", type="password")
    api_key_final = api_key_input
    if not api_key_input:
        st.sidebar.warning("⚠️ Requiere llave de acceso")

# 3. INTERFAZ GRÁFICA PRINCIPAL
st.image("https://images.unsplash.com/photo-1518770660439-4636190af475?auto=format&fit=crop&w=1200&q=80", use_container_width=True)

st.title("🧠 M3 Synthetic Board")
st.subheader("Plataforma Multiagente de Soporte a Decisiones Estratégicas")

col_kpi1, col_kpi2, col_kpi3, col_kpi4 = st.columns(4)
col_kpi1.metric(label="Agentes Convocados", value="8 Expertos")
col_kpi2.metric(label="Estructura de Datos", value="Agent Lake V1")
col_kpi3.metric(label="Tolerancia a Cuotas", value="Gestión Dinámica")
col_kpi4.metric(label="Límite por Agente", value="~150 palabras")

st.markdown("---")

st.markdown("### 📝 Caso de Negocio o Desafío Institucional")
caso_humano = st.text_area(
    "Instrucción: Ingrese la propuesta o el problema técnico que el comité sintético debe analizar, contrastar y documentar.",
    value="Evaluar si Misión 3 debe lanzar un reto de innovación abierta para mejorar la gestión de residuos en una municipalidad de Lima. Preparar recomendación, riesgos, aliados, campaña y plan operativo.",
    height=120,
    label_visibility="collapsed"
)

# FUNCIÓN DE LLAMADA CON SOPORTE COMPLETO PARA CONTROL DE ERRORES 429 Y 503
def consultar_agente_api_resiliente(client, nombre_agente: str, entrada: str, contexto: str = "") -> str:
    prompt_sistema = SYSTEM_PROMPTS.get(nombre_agente, "")
    contenido = f"Caso a evaluar: {entrada}\n\n"
    if contexto:
        contenido += f"Contexto y deliberación previa del comité:\n{contexto}"
        
    intentos_maximos = 3
    for intento in range(intentos_maximos):
        try:
            response = client.models.generate_content(
                model=model_choice,
                contents=contenido,
                config=types.GenerateContentConfig(
                    system_instruction=prompt_sistema,
                    temperature=0.2,
                ),
            )
            return response.text
        except Exception as e:
            error_msg = str(e).upper()
            # Si el error es por agotamiento de cuota (429) o saturación (503), pausamos la ejecución
            if "RESOURCE_EXHAUSTED" in error_msg or "429" in error_msg or "503" in error_msg:
                if intento < intentos_maximos - 1:
                    time.sleep(15)  # Pausa de seguridad para liberar la cuota por minuto de Google
                    continue
            raise e

# CONTROL DE EJECUCIÓN
if st.button("🚀 INICIAR DELIBERACIÓN ESTRATÉGICA", use_container_width=True):
    if not api_key_final:
        st.error("❌ Acción bloqueada: No se detecta una clave API válida para conectar con los agentes.")
    else:
        try:
            client = genai.Client(api_key=api_key_final)
            
            with st.status("🛸 Sincronizando Agent Lake y ejecutando consultas virtuales...", expanded=True) as status:
                
                st.write("🌐 `[Agente 1/7]` **Ecosistemas** analizando el impacto territorial...")
                op_ecosistemas = consultar_agente_api_resiliente(client, "ExpertoEcosistemas", caso_humano)
                time.sleep(1.0)
                
                st.write("🔬 `[Agente 2/7]` **Innovación** tasando el grado de novedad tecnológica...")
                op_innovacion = consultar_agente_api_resiliente(client, "ExpertoInnovacion", caso_humano)
                time.sleep(1.0)
                
                st.write("📈 `[Agente 3/7]` **Emprendimiento** evaluando el encaje problema-solución...")
                op_emprendimiento = consultar_agente_api_resiliente(client, "ExpertoEmprendimiento", caso_humano)
                time.sleep(1.0)
                
                st.write("🏛️ `[Agente 4/7]` **Vinculación U-E** mapeando laboratorios...")
                op_vinculacion = consultar_agente_api_resiliente(client, "ExpertoVinculacion", caso_humano)
                time.sleep(1.0)
                
                st.write("📋 `[Agente 5/7]` **Concursos** estructurando bases de postulación...")
                op_concursos = consultar_agente_api_resiliente(client, "ExpertoConcursos", caso_humano)
                time.sleep(1.0)
                
                st.write("📢 `[Agente 6/7]` **Comunicaciones** diseñando la narrativa estratégica...")
                op_comunicaciones = consultar_agente_api_resiliente(client, "ExpertoComunicaciones", caso_humano)
                time.sleep(1.0)
                
                st.write("⚙️ `[Agente 7/7]` **Automatización** modelando flujos digitales...")
                op_automatizacion = consultar_agente_api_resiliente(client, "ExpertoAutomatizacion", caso_humano)
                
                # PAUSA DE CONTROL ESTRATÉGICA PARA EL ORQUESTADOR
                st.write("⏳ `[Infraestructura]` Liberando cuota de tokens por minuto (RPM). Esperando 20 segundos antes del dictamen final...")
                time.sleep(20.0) 
                
                st.write("✍️ `[Orquestador]` **Secretario General** consolidando consensos, riesgos y dictando acta final...")
                
                memoria_deliberacion = (
                    f"### [Opinión] Experto en Ecosistemas\n{op_ecosistemas}\n\n"
                    f"### [Opinión] Experto en Innovación\n{op_innovacion}\n\n"
                    f"### [Opinión] Experto en Emprendimiento\n{op_emprendimiento}\n\n"
                    f"### [Opinión] Experto en Vinculación\n{op_vinculacion}\n\n"
                    f"### [Opinión] Experto en Concursos\n{op_concursos}\n\n"
                    f"### [Opinión] Experto en Comunicaciones\n{op_comunicaciones}\n\n"
                    f"### [Opinión] Experto en Automatización\n{op_automatizacion}\n\n"
                )
                
                prompt_secretario = (
                    f"Como Secretario General, procesa las opiniones de los 7 expertos sobre el caso '{caso_humano}'. "
                    f"Genera el documento oficial 'Acta del Comité Directivo Sintético M3' en Markdown, estructurando de "
                    f"forma estricta: Tema Evaluado, Agentes Participantes, Recomendaciones Clave consolidadas, "
                    f"Consensos Detectados, Disensos, Riesgos Identificados, Decisión Sugerida y un Plan de Acción Operativo paso a paso.\n\n"
                    f"Deliberación del comité:\n{memoria_deliberacion}"
                )
                
                acta_final = consultar_agente_api_resiliente(client, "SecretarioGeneral", prompt_secretario)
                status.update(label="⚡ Consolidación finalizada con éxito.", state="complete", expanded=False)
            
            st.session_state["acta_premium"] = acta_final
            st.session_state["lake_premium"] = memoria_deliberacion

        except Exception as e:
            st.error(f"Fallo en la comunicación agéntica por límites de cuota: {e}. Por favor, espere un momento e intente presionar el botón de nuevo.")

# 4. ENTREGA DE RESULTADOS DE ALTA FIDELIDAD
if "acta_premium" in st.session_state:
    st.markdown("### 🏆 Documento de Salida del Comité")
    
    tab_acta, tab_trazabilidad = st.tabs(["📜 Acta Ejecutiva Final", "🔍 Auditoría de Agent Lake"])
    
    with tab_acta:
        with st.container(border=True):
            st.markdown(st.session_state["acta_premium"])
            
        st.download_button(
            label="📥 EXPORTAR ACTA OFICIAL (MARKDOWN)",
            data=st.session_state["acta_premium"],
            file_name="acta_comite_m3.md",
            mime="text/markdown",
            use_container_width=True
        )
        
    with tab_trazabilidad:
        st.info("La siguiente información es el registro auditable de lo que cada experto opinó de forma independiente.")
        st.markdown(st.session_state["lake_premium"])
