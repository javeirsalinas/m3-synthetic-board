import streamlit as st
from google import genai
from google.genai import types

# CONFIGURACIÓN DE LA PÁGINA DE STREAMLIT
st.set_page_config(
    page_title="M3 Synthetic Board",
    page_icon="🤖",
    layout="wide"
)

# RECOLECCIÓN AUTOMÁTICA DE LA API KEY DESDE LOS SECRETOS SEGUROS
# Si no está configurado el secreto, se busca en la barra lateral como plan de respaldo
api_key_segura = st.secrets.get("GEMINI_API_KEY", "")

# SYSTEM PROMPTS (El "Agent Lake" con las 7 miradas expertas de Misión 3)
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
        "¿El Business Model Canvas es coherente? ¿Qué programa corresponde: preincubación, incubación o aceleración?"
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
        "Actúas como el Experto en Concursos y Programas de Misión 3. Diseña bases, criterios, cronogramas, "
        "jurados, beneficios, embudos y seguimiento. ¿Cómo mejorar las bases? ¿Qué criterios de evaluación usar? "
        "¿Cómo evitar sesgos regionales?"
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

# INTERFAZ DE USUARIO: BARRA LATERAL
st.sidebar.title("⚙️ Configuración")
model_choice = st.sidebar.selectbox("Modelo Core", ["gemini-2.5-flash", "gemini-2.5-pro"])

# Si el secreto no fue cargado correctamente, mostramos una advertencia e input de respaldo
if not api_key_segura:
    api_key_input = st.sidebar.text_input("Gemini API Key (Respaldo)", type="password")
    api_key_final = api_key_input
else:
    st.sidebar.success("🔑 API Key cargada automáticamente desde Secrets.")
    api_key_final = api_key_segura

# INTERFAZ DE USUARIO: ÁREA PRINCIPAL
st.title("🤖 M3 Synthetic Board")
st.caption("Comité Directivo Agéntico de Misión 3 — Infraestructura Multiagente para Decisiones Estratégicas")

caso_humano = st.text_area(
    "📝 Describa el caso, reto o iniciativa a evaluar por el Comité Directivo Sintético:",
    value="Evaluar si Misión 3 debe lanzar un reto de innovación abierta para mejorar la gestión de residuos en una municipalidad de Lima. Preparar recomendación, riesgos, aliados, campaña y plan operativo.",
    height=120
)

# FUNCIÓN DE LLAMADA TÉCNICA A CADA AGENTE
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
            temperature=0.2, # Disminuido a 0.2 para asegurar consistencia corporativa
        ),
    )
    return response.text

# EJECUCIÓN SÍNCRONA DEL COMITÉ
if st.button("🚀 Convocar Comité Directivo Sintético"):
    if not api_key_final:
        st.error("Error: No se detectó ninguna Gemini API Key. Configúrala en los Secrets de Streamlit o en la barra lateral.")
    else:
        try:
            client = genai.Client(api_key=api_key_final)
            
            with st.status("⏳ Comité Directivo en sesión. Procesando análisis de expertos...", expanded=True) as status:
                
                st.write("🕵️‍♂️ 1/7 Analizando Entorno Territorial (Ecosistemas)...")
                op_ecosistemas = consultar_agente_api(client, "ExpertoEcosistemas", caso_humano)
                
                st.write("🔬 2/7 Evaluando viabilidad técnica y madurez (Innovación)...")
                op_innovacion = consultar_agente_api(client, "ExpertoInnovacion", caso_humano)
                
                st.write("💼 3/7 Evaluando modelo de negocio y escalabilidad (Emprendimiento)...")
                op_emprendimiento = consultar_agente_api(client, "ExpertoEmprendimiento", caso_humano)
                
                st.write("🏛️ 4/7 Vinculando capacidades académicas e investigadores (Universidad-Empresa)...")
                op_vinculacion = consultar_agente_api(client, "ExpertoVinculacion", caso_humano)
                
                st.write("📋 5/7 Diseñando estructura de bases y evaluación (Concursos)...")
                op_concursos = consultar_agente_api(client, "ExpertoConcursos", caso_humano)
                
                st.write("📢 6/7 Estructurando narrativa pública y canales (Comunicaciones)...")
                op_comunicaciones = consultar_agente_api(client, "ExpertoComunicaciones", caso_humano)
                
                st.write("⚙️ 7/7 Trazando flujos digitales y herramientas (Automatización)...")
                op_automatizacion = consultar_agente_api(client, "ExpertoAutomatizacion", caso_humano)
                
                st.write("✍️ Secretario General analizando posturas y redactando el Acta del Comité...")
                
                # Consolidación completa de las minutas en la memoria del Agent Lake
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
                status.update(label="✅ Sesión concluida. Acta oficial generada.", state="complete", expanded=False)
            
            # Guardamos los resultados en la sesión para evitar pérdida de datos por recargas
            st.session_state["acta_comite_completa"] = acta_final
            st.session_state["trazabilidad_lake"] = memoria_deliberacion

        except Exception as e:
            st.error(f"Ocurrió un error en la ejecución del comité: {e}")

# DESPLIEGUE EN PANTALLA DE LOS DOCUMENTOS DE SALIDA
if "acta_comite_completa" in st.session_state:
    st.success("### 📜 Acta de Decisión — Comité Directivo Sintético M3")
    st.markdown(st.session_state["acta_comite_completa"])
    
    st.divider()
    
    with st.expander("🔍 Revisar Trazabilidad Agéntica Completa (Agent Lake)"):
        st.markdown(st.session_state["trazabilidad_lake"])
        
    st.download_button(
        label="📥 Descargar Acta de Comité (.md)",
        data=st.session_state["acta_comite_completa"],
        file_name="acta_comite_m3_completo.md",
        mime="text/markdown"
    )
