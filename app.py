import streamlit as st
from google import genai
from google.genai import types

# CONFIGURACIÓN DE LA PÁGINA DE STREAMLIT
st.set_page_config(
    page_title="M3 Synthetic Board",
    page_icon="🤖",
    layout="wide"
)

# SYSTEM PROMPTS (Memoria técnica y directrices de cada agente)
SYSTEM_PROMPTS = {
    "SecretarioGeneral": (
        "Actúas como Secretario Técnico del Comité Directivo de Misión 3. "
        "Tu rol es coordinar la deliberación, exigir evidencia a los expertos, "
        "identificar consensos y disensos, y preparar un Acta y Recomendación Ejecutiva "
        "estructurada en Markdown para validación humana final."
    ),
    "ExpertoEcosistemas": (
        "Actúas como el Experto en Ecosistemas de Misión 3. Evalúas el contexto nacional, "
        "regional, sectorial e institucional. Responde: ¿Qué impacto tendría esta iniciativa en el ecosistema? "
        "¿Qué actores (regiones, gremios, universidades) son relevantes? ¿Cómo se alinea con la tercera misión universitaria?"
    ),
    "ExpertoEmprendimiento": (
        "Actúas como el Experto en Emprendimiento de Misión 3. Evalúas la calidad de "
        "las propuestas, modelos de negocio, tracción y escalabilidad. Responde: ¿La propuesta resuelve un problema real? "
        "¿Es coherente el modelo de negocio? ¿Qué programa corresponde: preincubación, incubación o aceleración?"
    ),
    "ExpertoInnovacion": (
        "Actúas como el Experto en Innovación de Misión 3. Evalúas novedad, diferenciación, "
        "madurez tecnológica y potencial de transferencia. Responde: ¿La solución es innovación incremental, "
        "sustancial o disruptiva? ¿Cuál es su nivel de madurez y qué riesgos técnicos existen?"
    )
}

# INTERFAZ DE USUARIO: BARRA LATERAL
st.sidebar.title("⚙️ Configuración")
api_key_input = st.sidebar.text_input("Gemini API Key", type="password", help="Introduce tu clave de Google AI Studio")
model_choice = st.sidebar.selectbox("Modelo Core", ["gemini-2.5-flash", "gemini-2.5-pro"])

# INTERFAZ DE USUARIO: ÁREA PRINCIPAL
st.title("🤖 M3 Synthetic Board")
st.caption("Comité Directivo Agéntico de Misión 3 — Simulación y Trazabilidad de Decisiones")

st.markdown("""
Este sistema multiagente activa diferentes perspectivas expertas para analizar una propuesta institucional.
El objetivo es contrastar enfoques y generar un acta detallada para asistir la toma de decisiones humana.
""")

# Input del caso a evaluar
caso_humano = st.text_area(
    "📝 Describa la iniciativa o reto a evaluar por el Comité:",
    value="Evaluar si Misión 3 debe lanzar un reto de innovación abierta para mejorar la gestión de residuos en una municipalidad de Lima. Preparar recomendación, riesgos y aliados clave.",
    height=100
)

# FUNCIÓN AUXILIAR DE CONSULTA A LA API
def consultar_agente_api(client, nombre_agente: str, entrada: str, contexto: str = "") -> str:
    prompt_sistema = SYSTEM_PROMPTS.get(nombre_agente, "")
    contenido = f"Caso a evaluar: {entrada}\n\n"
    if contexto:
        contenido += f"Contexto y opiniones previas del comité:\n{contexto}"
        
    response = client.models.generate_content(
        model=model_choice,
        contents=contenido,
        config=types.GenerateContentConfig(
            system_instruction=prompt_sistema,
            temperature=0.3,
        ),
    )
    return response.text

# BOTÓN DE ACCIÓN PARA DISPARAR EL COMITÉ
if st.button("🚀 Iniciar Deliberación del Comité"):
    if not api_key_input:
        st.error("Por favor, introduce una API Key válida en la barra lateral antes de continuar.")
    else:
        try:
            # Inicializamos el cliente con la llave provista por la interfaz web
            client = genai.Client(api_key=api_key_input)
            
            # Contenedor de estado dinámico de Streamlit para simular la sesión
            with st.status("⏳ Comité en sesión. Los agentes están deliberando...", expanded=True) as status:
                
                st.write("🕵️‍♂️ Consultando al Experto en Ecosistemas...")
                op_ecosistemas = consultar_agente_api(client, "ExpertoEcosistemas", caso_humano)
                
                st.write("🔬 Consultando al Experto en Innovación...")
                op_innovacion = consultar_agente_api(client, "ExpertoInnovacion", caso_humano)
                
                st.write("💼 Consultando al Experto en Emprendimiento...")
                op_emprendimiento = consultar_agente_api(client, "ExpertoEmprendimiento", caso_humano)
                
                st.write("✍️ Secretario General consolidando minutas y redactando el acta...")
                
                # Consolidación de la memoria del "Agent Lake"
                memoria_deliberacion = (
                    f"--- OPINIÓN EXPERTO ECOSISTEMAS ---\n{op_ecosistemas}\n\n"
                    f"--- OPINIÓN EXPERTO INNOVACIÓN ---\n{op_innovacion}\n\n"
                    f"--- OPINIÓN EXPERTO EMPRENDIMIENTO ---\n{op_emprendimiento}\n\n"
                )
                
                prompt_secretario = (
                    f"Como Secretario General, procesa las siguientes opiniones de los expertos sobre el caso '{caso_humano}'. "
                    f"Genera el documento oficial 'Acta del Comité Directivo Sintético M3' en Markdown, identificando "
                    f"claramente Consensos, Disensos, Riesgos y el Plan de acción final.\n\n"
                    f"Deliberación técnica:\n{memoria_deliberacion}"
                )
                
                acta_final = consultar_agente_api(client, "SecretarioGeneral", prompt_secretario)
                status.update(label="✅ Deliberación Finalizada. Acta generada.", state="complete", expanded=False)
            
            # GUARDAR EN EL ESTADO DE LA SESIÓN PARA EVITAR BORRADOS
            st.session_state["acta_comite"] = acta_final
            st.session_state["deliberacion_detallada"] = memoria_deliberacion

        except Exception as e:
            st.error(f"Ocurrió un error al conectar con Gemini: {e}")

# DESPLIEGUE DE RESULTADOS (Si existen en la sesión)
if "acta_comite" in st.session_state:
    st.success("### 📜 Acta Oficial del Comité Directivo Sintético M3")
    
    # Mostramos el Markdown renderizado directamente de manera elegante
    st.markdown(st.session_state["acta_comite"])
    
    st.divider()
    
    # Pestaña secundaria para revisar la trazabilidad técnica ("Agent Lake")
    with st.expander("🔍 Ver anexo de trazabilidad (Opiniones individuales sin procesar)"):
        st.text(st.session_state["deliberacion_detallada"])
        
    # BOTÓN DE DESCARGA
    st.download_button(
        label="📥 Descargar Acta en formato Markdown (.md)",
        data=st.session_state["acta_comite"],
        file_name="acta_comite_m3.md",
        mime="text/markdown"
    )
