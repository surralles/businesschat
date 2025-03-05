import streamlit as st
from langchain_ollama import OllamaLLM
from langchain_core.prompts import ChatPromptTemplate
from negocio_info import store_data

st.title("🧞‍♀️Tu asistente en Algorithmics")


if "messages" not in st.session_state:
    st.session_state.messages = []
if "first_message" not in st.session_state:
    st.session_state.first_message = True

if "context" not in st.session_state:
    st.session_state.context = ""

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if st.session_state.first_message:
    with st.chat_message("assistant"):
        st.markdown("Hola, ¿cómo puedo ayudarte")

    st.session_state.messages.append(
        {"role": "assistant", "content": "Hola, ¿cómo puedo ayudarte"}
    )
    st.session_state.first_message = False

if "ollama" not in st.session_state:

    template = """"
    Responde de manera clara y profesional en español. No agregues comentarios innecesarios ni advertencias.


    Aquí está la información del negocio:
    {negocio_info}

    Historial de conversación:
    {context}

    Pregunta del usuario: {question}

    Respuesta:

    """

    model = OllamaLLM(model="llama3.2:1b")
    prompt = ChatPromptTemplate.from_template(template)
    st.session_state.ollama = prompt | model


if prompt := st.chat_input("¿cómo puedo ayudarte?"):
    with st.chat_message("user"):
        st.markdown(prompt)

    st.session_state.messages.append({"role": "user", "content": prompt})

    result = st.session_state.ollama.invoke(
        {
            "negocio_info": store_data,
            "context": st.session_state.context,
            "question": prompt,
        }
    )

    with st.chat_message("assistant"):
        st.markdown(result)

    st.session_state.messages.append({"role": "assistant", "content": result})

    st.session_state.context += f"Bot: {result}\nYou:{prompt}\n "
