import streamlit as st
import requests
from negocio_info import store_data

# URL de la API de Ollama en Fly.io (reemplázala con la tuya)
OLLAMA_API_URL = "https://mi-ollama-server.fly.dev"

st.title("🧞‍♀️Tu asistente en Algorithmics")

# Inicializar variables de sesión
if "messages" not in st.session_state:
    st.session_state.messages = []
if "first_message" not in st.session_state:
    st.session_state.first_message = True
if "context" not in st.session_state:
    st.session_state.context = ""

# Mostrar mensajes anteriores
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Mensaje de bienvenida
if st.session_state.first_message:
    with st.chat_message("assistant"):
        st.markdown("Hola, ¿cómo puedo ayudarte?")

    st.session_state.messages.append(
        {"role": "assistant", "content": "Hola, ¿cómo puedo ayudarte?"}
    )
    st.session_state.first_message = False


def chat_with_ollama(prompt, context, negocio_info):
    data = {
        "model": "llama3.2:1b",
        "prompt": f"""Responde de manera clara y profesional en español.

        Aquí está la información del negocio:
        {negocio_info}

        Historial de conversación:
        {context}

        Pregunta del usuario: {prompt}

        Respuesta:
        """,
        "stream": False,  # Cambiar a True si quieres streaming de respuestas
    }

    try:
        response = requests.post(f"{OLLAMA_API_URL}/api/generate", json=data)
        response.raise_for_status()  # Lanza un error si hay problemas con la API
        return response.json()["response"]
    except requests.exceptions.RequestException as e:
        return f"Error al conectar con Ollama: {e}"


# Capturar entrada del usuario
if prompt := st.chat_input("¿Cómo puedo ayudarte?"):
    with st.chat_message("user"):
        st.markdown(prompt)

    st.session_state.messages.append({"role": "user", "content": prompt})

    # Llamar a la API de Ollama
    result = chat_with_ollama(prompt, st.session_state.context, store_data)

    with st.chat_message("assistant"):
        st.markdown(result)

    st.session_state.messages.append({"role": "assistant", "content": result})

    # Actualizar contexto
    st.session_state.context += f"Bot: {result}\nYou: {prompt}\n"
