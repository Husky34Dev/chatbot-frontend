import streamlit as st
from transformers import AutoTokenizer, AutoModelForCausalLM, TextStreamer
from huggingface_hub import login
import requests
import sseclient
import json

st.set_page_config(page_title="Agente Chatbot", page_icon="🤖")
st.title("🤖 Agente Chatbot Inteligente")
st.write("Pregunta lo que quieras sobre abonados y el agente consultará la base de datos en tiempo real.")

# Dirección de tu backend en Render
BACKEND_MCP_URL = "https://agent-mcp-demo.onrender.com/mcp"  # <-- cámbiala por la tuya real

# Modelo (puedes cambiar a otro si prefieres)
MODEL_NAME = "TinyLlama/TinyLlama-1.1B-Chat-v1.0"

@st.cache_resource
def load_model():
    tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME)
    model = AutoModelForCausalLM.from_pretrained(MODEL_NAME, torch_dtype="auto")
    return tokenizer, model

tokenizer, model = load_model()

if "history" not in st.session_state:
    st.session_state.history = []

user_input = st.text_input("Tú:", key="user_input")

if st.button("Enviar") and user_input:
    st.session_state.history.append(("🧑‍💬", user_input))

    # Instrucción para el agente
    system_prompt = (
        "Eres un agente inteligente que responde preguntas sobre facturas y datos personales. "
        "Usa las herramientas MCP disponibles para obtener la información necesaria y responde de forma clara."
    )
    full_input = system_prompt + "\n\nUsuario: " + user_input

    # Petición al backend vía SSE
    try:
        response = requests.post(
            BACKEND_MCP_URL,
            stream=True,
            headers={"Content-Type": "application/json"},
            data=json.dumps({"input": user_input})
        )
        client = sseclient.SSEClient(response)
        msg = ""
        for event in client.events():
            if event.event == "complete":
                resultado = json.loads(event.data)
                msg = resultado["data"][0]["respuesta"]
                break
        if not msg:
            msg = "⚠️ No se recibió respuesta del backend."
    except Exception as e:
        msg = f"❌ Error de conexión: {e}"

    st.session_state.history.append(("🤖", msg))

# Mostrar historial
for speaker, text in reversed(st.session_state.history):
    with st.chat_message(speaker):
        st.markdown(text)