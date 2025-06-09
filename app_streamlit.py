
import streamlit as st
import requests

st.set_page_config(page_title="Chatbot de Consultas", page_icon="🤖")

st.title("🤖 Chatbot de Consultas de Abonados")
st.write("Haz una pregunta sobre un abonado y te devolverá la intención y datos extraídos.")

if "messages" not in st.session_state:
    st.session_state.messages = []

user_input = st.text_input("Tu mensaje:", key="input")

if st.button("Enviar") and user_input:
    st.session_state.messages.append(("🧑‍💬 Tú", user_input))

    try:
        response = requests.post(
            "https://TU_NOMBRE_DE_RENDER.onrender.com/extraer",
            json={"mensaje": user_input}
        )
        if response.status_code == 200:
            result = response.json()["data"][0]
            text = f"**Intención:** {result['intencion']}\n**Tipo de dato:** {result['tipo_dato']}\n**Valor:** {result['valor_dato']}"
        else:
            text = "❌ Error al procesar la respuesta."
    except Exception as e:
        text = f"⚠️ Error de conexión: {e}"

    st.session_state.messages.append(("🤖 Chatbot", text))

for sender, msg in reversed(st.session_state.messages):
    with st.chat_message(sender):
        st.markdown(msg)
