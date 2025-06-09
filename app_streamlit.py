import streamlit as st
import requests

# Configuración de la página
st.set_page_config(page_title="Chatbot de Consultas de Abonados", page_icon="🤖")

st.title("🤖 Chatbot de Consultas de Abonados")
st.write("Haz una pregunta sobre un abonado y te devolverá la respuesta directamente desde la base de datos.")

# Historial de mensajes
if "messages" not in st.session_state:
    st.session_state.messages = []

# Entrada del usuario
user_input = st.text_input("Tu mensaje:", key="input")

# Acción al pulsar el botón
if st.button("Enviar") and user_input:
    st.session_state.messages.append(("🧑‍💬 Tú", user_input))

    try:
        # CAMBIA ESTA URL por la de tu backend en Render
        response = requests.post(
            "https://chatbot-agent.onrender.com/extraer",
            json={"mensaje": user_input}
        )
        if response.status_code == 200:
            result = response.json()["data"][0]
            text = result["respuesta"]
        else:
            text = "❌ Error al procesar la respuesta."
    except Exception as e:
        text = f"⚠️ Error de conexión: {e}"

    st.session_state.messages.append(("🤖 Chatbot", text))

# Mostrar conversación
for sender, msg in reversed(st.session_state.messages):
    with st.chat_message(sender):
        st.markdown(msg)
