import streamlit as st
from streamlit_lottie import st_lottie
import requests
from ChatBot import Asistente

def load_lottieurl(url: str):
    r = requests.get(url)
    if r.status_code != 200:
        return None
    return r.json()

def main():
    st.set_page_config(page_title="Chatbot con Streamlit", page_icon="🚀", layout="centered")

    if 'chat_started' not in st.session_state:
        st.session_state.chat_started = False
    
    lottie_url = "https://lottie.host/6ffa7e41-5f8f-4fc2-a715-3227c0711761/d0OgkMKnWB.json"
    lottie_animation = load_lottieurl(lottie_url)

    if not st.session_state.chat_started:
        st.markdown(
            """
            <style>
            .container {
                display: flex;
                flex-direction: column;
                align-items: center;
                justify-content: center;
                height: 0vh;
                text-align: center;
            }
            h1 {
                margin-bottom: 20px;
            }
            .start-button {
                margin-top: 60px;
            }
            </style>
            """,
            unsafe_allow_html=True
        )

        st.markdown('<div class="container">', unsafe_allow_html=True)

        if lottie_animation:
            st_lottie(lottie_animation, height=200)

        st.markdown('<h1>Bienvenido al chatbot de la corporación</h1>', unsafe_allow_html=True)
        st.write("Este chat está capacitado para trabajar en conjunto con los empleados de La Asociación Pro-Desarrollo Comunal del Patio Inc.")
        
        if st.button("Start", key="start_button", help="Haz clic para iniciar"):
            st.session_state.chat_started = True

        st.markdown('</div>', unsafe_allow_html=True)
    else:
        chat_interface()

def chat_interface():
    st.title('🚀 Asistente virtual')

    if 'messages' not in st.session_state:
        st.session_state.messages = []
    if 'first_message' not in st.session_state:
        st.session_state.first_message = True

    for message in st.session_state.messages:
        with st.chat_message(message['role']):
            st.markdown(message['content'])

    if st.session_state.first_message:
        with st.chat_message('assistant'):
            st.markdown('Hola, ¿Cómo puedo ayudarte?')

        st.session_state.messages.append({'role':"assistant", "content": 'Hola, ¿Cómo puedo ayudarte?'})
        st.session_state.first_message = False

    if promt := st.chat_input("¿Cómo puedo ayudarte?"):
        with st.chat_message("user"):
            st.markdown(promt)
        st.session_state.messages.append({'role':"user", "content": promt})

        with st.chat_message("assistant"):
            response = Asistente().chat(promt)
            st.markdown(response)
        st.session_state.messages.append({'role':"assistant", "content": response})

if __name__ == "__main__":
    main()