import streamlit as st
from google import genai
from google.genai import types

# 1. CONFIGURACIÓN DE MAQUETACIÓN PREMIUM
st.set_page_config(
    page_title="M3 Synthetic Board | Centro de Comando",
    page_icon="🧠",
    layout="wide",
    initial_sidebar_state="expanded"
)

# RECOLECCIÓN DE CREDENCIALES SEGURAS
api_key_segura = st.secrets.get("GEMINI_API_KEY", "")

# SYSTEM PROMPTS (Diccionario de Agentes)
SYSTEM_PROMPTS = {
    "SecretarioGeneral": (
        "Actúas como Secretario Técnico del Comité Directivo de Misión 3. Organiza la deliberación "
        "entre agentes expertos, exige evidencia, identifica consensos y disensos, y prepara una "
        "recomendación ejecutiva estructurada en Markdown para validación humana."
    ),
    "ExpertoEcosistemas": (
        "Actúas como el Experto en Ecosistemas de Misión 3. Evalúas el contexto nacional, regional, "
        "sectorial e institucional. ¿Qué impacto tendría esta iniciativa en el ecosistema? ¿Qué actores "
        "deberían participar (regiones, gremios, cámaras, universidades)? ¿Cómo se alinea con la tercera misión universitaria?"
    ),
    "ExpertoEmprendimiento": (
        "Actúas como el Experto en Emprendimiento de Misión 3. Evalúas la calidad de las propuestas, "
        "modelos de negocio, equipos, tracción y escalabilidad. ¿La propuesta tiene un problema real? "
        "Análisis rápido del modelo de negocio. ¿Qué programa corresponde: preincubación, incubación o aceleración?"
    ),
    "ExpertoInnovacion": (
        "Actúas como el Experto en Innovación de Misión 3. Evalúas novedad, diferenciación, madurez tecnológica "
        "y potencial de transferencia. ¿La solución es innovación incremental, sustancial o disruptiva? ¿Tiene base "
        "tecnológica o científica? ¿Cuál es su nivel de madurez y qué riesgos técnicos existen?"
    ),
    "ExpertoVinculacion": (
        "Actúas como el Experto en Vinculación Universidad-Empresa de Misión 3. Conecta oferta académica, "
        "investigación, empresas y retos del mercado. ¿Qué facultades o laboratorios pueden participar? "
        "¿Qué empresas se benefician? ¿Cómo convertir conocimiento académico en valor empresarial?"
    ),
    "ExpertoConcursos": (
        "Actúas como el Experto en Concursos y Programas de Misión 3. Diseña bases, criteria, cronogramas, "
        "jurados, beneficios, embudos y seguimiento. ¿Cómo mejorar las bases? ¿Qué criterios de evaluación usar? "
        "Análisis de sesgos."
    ),
    "ExpertoComunicaciones": (
        "Actúas como el Experto en Comunicaciones de Misión 3. Convierte la decisión en narrativa, campaña, "
        "mailing, LinkedIn, notas de prensa y mensajes institucionales. ¿Cuál es el mensaje estratégico? "
        "¿Qué tono usar? ¿Cómo convertir una decisión técnica en una campaña movilizadora?"
    ),
    "ExpertoAutomatizacion": (
        "Actúas como el Experto en Automatización de Procesos de Misión 3. Traduce la decisión en flujos, "
        "formularios, dashboards, integraciones y tareas automáticas. ¿Qué proceso se puede automatizar? "
        "¿Qué herramientas usar? ¿Qué partes requieren aprobación humana?"
    )
}

# 2. SECCIÓN LATERAL DE CONTROL (SIDEBAR)
st.sidebar.image("https://img.icons8.com/fluent/96/000000/artificial-intelligence.png", width=60)
st.sidebar.title("M3 Control Panel")
st.sidebar.markdown("---")

model_choice = st.sidebar.selectbox(
    "🤖 Motor de Inteligencia", 
    ["gemini-2.5-flash", "gemini-2.5-pro"],
    help="Elige el modelo cerebral para la deliberación. Pro ofrece mayor profundidad analítica."
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

# 3. INTERFAZ GRÁFICA PRINCIPAL (HERO SECTION)
# Imagen conceptual de agentes de IA en reunión con estética futurista y atractiva
st.image("https://images.unsplash.com/photo-1618005182384-a83a8bd57fbe?auto=format&fit=crop&w=1200&q=80", use_container_width=True)

st.title("🧠 M3 Synthetic Board")
st.subheader("Plataforma Multiagente de Soporte a Decisiones Estratégicas")

# KPIs de Estado de la Plataforma (UX/UI de Dashboard Corporativo)
col_kpi1, col_kpi2, col_kpi3, col_kpi4 = st.columns(4)
col_kpi1.metric(label="Agentes Convocados", value="8 Expertos")
col_kpi2.metric(label="Estructura de Datos", value="Agent Lake V1")
col_kpi3.metric(label="Nivel de Supervisión", value="Jerárquico")
col_kpi4.metric(label="Rol Humano", value="Validador Final")

st.markdown("---")

# ZONA DE TRABAJO (Entrada de Datos)
st.markdown("### 📝 Caso de Negocio o Desafío Institucional")
caso_humano = st.text_area(
    "Instrucción: Ingrese la propuesta o el problema técnico que el comité sintético debe analizar, contrastar y documentar.",
    value="Evaluar si Misión 3 debe lanzar un reto de innovación abierta para mejorar la gestión de residuos en una municipalidad de Lima. Preparar recomendación, riesgos, aliados, campaña y plan operativo.",
    height=120,
    label_visibility="collapsed"
)

# FUNCIÓN TÉCNICA DE LLAMADA
def consultar_agente_api(client, nombre_agente: str, entrada: str, contexto: str = "") -> str:
    prompt_sistema = SYSTEM_PROMPTS.get(nombre_agente, "")
    contenido = f"Caso a evaluar: {entrada}\n\n"
    if contexto:
        contenido += f"Contexto y deliberación previa del comité:\n{contexto}"
        
    response = client.models.generate_content(
        model=model_choice,
        contents=contenido,
        config=types.GenerateContentConfig(
            system_instruction=prompt_sistema,
            temperature=0.2,
        ),
    )
    return response.text

# CONTROL DE EJECUCIÓN CON DISEÑO MEJORADO
if st.button("🚀 INICIAR DELIBERACIÓN ESTRATÉGICA", use_container_width=True):
    if not api_key_final:
        st.error("❌ Acción bloqueada: No se detecta una clave API válida para conectar con los agentes.")
    else:
        try:
            client = genai.Client(api_key=api_key_final)
            
            # Animación e historial de ejecución visual interactiva
            with st.status("🛸 Sincronizando Agent Lake y ejecutando consultas virtuales...", expanded=True) as status:
                
                st.write("🌐 `[Agente 1/7]` **Ecosistemas** analizando el impacto territorial y actores clave...")
                op_ecosistemas = consultar_agente_api(client, "ExpertoEcosistemas", caso_humano)
                
                st.write("🔬 `[Agente 2/7]` **Innovación** tasando el grado de novedad tecnológica...")
                op_innovacion = consultar_agente_api(client, "ExpertoInnovacion", caso_humano)
                
                st.write("📈 `[Agente 3/7]` **Emprendimiento** evaluando el encaje problema-solución...")
                op_emprendimiento = consultar_agente_api(client, "ExpertoEmprendimiento", caso_humano)
                
                st.write("🏛️ `[Agente 4/7]` **Vinculación U-E** mapeando laboratorios y oferta académica...")
                op_vinculacion = consultar_agente_api(client, "ExpertoVinculacion", caso_humano)
                
                st.write("📋 `[Agente 5/7]` **Concursos** estructurando bases de postulación sugeridas...")
                op_concursos = consultar_agente_api(client, "ExpertoConcursos", caso_humano)
                
                st.write("📢 `[Agente 6/7]` **Comunicaciones** diseñando la narrativa estratégica pública...")
                op_comunicaciones = consultar_agente_api(client, "ExpertoComunicaciones", caso_humano)
                
                st.write("⚙️ `[Agente 7/7]` **Automatización** modelando flujos y dashboards de captura...")
                op_automatizacion = consultar_agente_api(client, "ExpertoAutomatizacion", caso_humano)
                
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
                    f"Consensos Detectados, Disensos/Puntos de Fricción, Riesgos Identificados, Decisión Sugerida "
                    f"y un Plan de Acción Operativo paso a paso.\n\n"
                    f"Deliberación del comité:\n{memoria_deliberacion}"
                )
                
                acta_final = consultar_agente_api(client, "SecretarioGeneral", prompt_secretario)
                status.update(label="⚡ Consolidación finalizada con éxito.", state="complete", expanded=False)
            
            st.session_state["acta_premium"] = acta_final
            st.session_state["lake_premium"] = memoria_deliberacion

        except Exception as e:
            st.error(f"Fallo en la comunicación agéntica: {e}")

# 4. ENTREGA DE RESULTADOS DE ALTA FIDELIDAD (OUTPUT UX)
if "acta_premium" in st.session_state:
    st.markdown("### 🏆 Documento de Salida del Comité")
    
    # Dividimos la visualización en Pestañas para mejorar la carga cognitiva del usuario
    tab_acta, tab_trazabilidad = st.tabs(["📜 Acta Ejecutiva Final", "🔍 Auditoría de Agent Lake"])
    
    with tab_acta:
        # Contenedor visual destacado con un diseño limpio
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
