import os
import streamlit as st
from openai import OpenAI

st.set_page_config(page_title="Vox | Tutor de programación", page_icon="🤖", layout="wide")

SYSTEM_PROMPT = """
Eres Vox, un agente conversacional educativo especializado en programación para estudiantes.
Ayuda a comprender, practicar y estudiar, no solo a entregar respuestas.
Temas: fundamentos, POO, estructuras de datos, depuración de código en Python, Java,
JavaScript, C/C++ y SQL, y preparación para exámenes.
Responde en español salvo que pidan otro idioma. Explica claramente y adapta el nivel
a principiantes cuando sea necesario. Al mostrar código, indica el lenguaje y explica
por qué funciona. No afirmes que ejecutaste código si no lo hiciste. En modo estudio,
haz preguntas una por una y espera el intento del estudiante.
"""

MODE_INSTRUCTIONS = {
    "Tutor de programación": "Resuelve dudas y ofrece ejemplos graduales.",
    "Modo de estudio": "Actúa como tutor: haz preguntas una por una y espera respuestas.",
    "Revisión de código": "Analiza el código compartido, explica errores y mejoras; no afirmes ejecutarlo.",
    "Práctica para examen": "Haz preguntas tipo examen una por una y ofrece retroalimentación.",
}

def get_api_key():
    key = os.getenv("OPENAI_API_KEY", "").strip()
    if key:
        return key
    try:
        return str(st.secrets["OPENAI_API_KEY"]).strip()
    except Exception:
        return ""

def get_setting(name, default):
    try:
        return str(st.secrets.get(name, default))
    except Exception:
        return os.getenv(name, default)

api_key = get_api_key()
model = get_setting("OPENAI_MODEL", "gpt-4.1-mini")
tts_model = get_setting("OPENAI_TTS_MODEL", "gpt-4o-mini-tts")
transcription_model = get_setting("OPENAI_TRANSCRIPTION_MODEL", "gpt-4o-mini-transcribe")

st.markdown("""
<style>
:root {
  --bg:#0c0d14; --panel:#151724; --line:#292b43;
  --purple:#6157ed; --blue:#777cff; --text:#f1f0fa; --muted:#a6a6bd;
}
.stApp { background: radial-gradient(ellipse at 50% 43%, #171b3b 0%, #0d0e15 52%); color:var(--text); }
header[data-testid="stHeader"] { background:rgba(12,13,20,.92); }
.block-container { max-width: 1120px; padding: 2.8rem 1.5rem 2rem; }
[data-testid="stSidebar"] { background:#10111a; border-right:1px solid #25263a; }
[data-testid="stSidebar"] > div:first-child { padding-top:1.1rem; }
.vox-brand {display:flex;align-items:center;gap:11px;padding:5px 0 22px;}
.vox-logo {width:42px;height:42px;border-radius:14px;display:flex;align-items:center;justify-content:center;font-size:23px;background:linear-gradient(135deg,#5147db,#777cff);box-shadow:0 5px 22px #5147db38;}
.vox-title {font-size:25px;font-weight:750;letter-spacing:-.7px;line-height:1.05;}
.vox-sub {font-size:12px;color:var(--muted);margin-top:4px;}
.vox-welcome {text-align:center; padding: min(13vh,105px) 0 18px;}
.vox-welcome h1 {font-size:clamp(28px,3.4vw,42px);font-weight:500;letter-spacing:-1.2px;margin:0;color:#efeffa;}
.vox-welcome p {font-size:16px;color:var(--muted);margin:13px 0 30px;}
.vox-status {display:inline-flex;align-items:center;gap:7px;color:#c4c4df;border:1px solid #333650;border-radius:999px;padding:6px 11px;font-size:12px;background:#191a2a;}
.vox-status-dot {width:7px;height:7px;background:#8b88ff;border-radius:50%;}
.stButton > button {border-radius:999px!important;border:1px solid #34354d!important;background:#191a27!important;color:#e6e5f5!important;min-height:42px;white-space:nowrap!important;padding:0 .85rem!important;font-size:14px!important;}
.stButton > button:hover {border-color:#7169fa!important;background:#24253c!important;}
.stButton > button[kind="primary"] {background:linear-gradient(110deg,#5147db,#6966f4)!important;border:0!important;color:white!important;}
.stTextInput input,.stTextArea textarea,.stSelectbox div[data-baseweb="select"] > div {background:#191a27!important;border-color:#34354d!important;border-radius:12px!important;color:#f4f3ff!important;}
[data-testid="stChatMessage"] {background:rgba(22,23,37,.86);border:1px solid #292b42;border-radius:18px;padding:15px 18px;margin:12px 0;}
[data-testid="stChatMessage"]:has([data-testid="chatAvatarIcon-assistant"]) {background:rgba(19,20,33,.88);}
[data-testid="stChatInput"] {border:1px solid #383a55!important;border-radius:999px!important;background:#1d1e29!important;box-shadow:0 8px 32px #00000025;}
[data-testid="stChatInput"] textarea {color:#f4f3ff!important;}
[data-testid="stChatInput"] textarea::placeholder {color:#aaaac0!important;}
[data-testid="stPopover"] button {border-radius:999px!important;}
/* El primer popover del contenido principal es "Acerca de"; fijarlo en la zona superior.
   Se coloca antes que el resto de popovers en el código para que este selector sea estable. */
section.main div[data-testid="stPopover"]:first-of-type {
  position: fixed !important;
  top: .55rem !important;
  right: 6.1rem !important;
  z-index: 100000 !important;
  width: auto !important;
  margin: 0 !important;
}
section.main div[data-testid="stPopover"]:first-of-type > button {
  min-height: 32px !important;
  height: 32px !important;
  padding: 0 .85rem !important;
  font-size: 13px !important;
  background: #191a27 !important;
  border: 1px solid #34354d !important;
  border-radius: 999px !important;
}
@media (max-width: 700px) {
  section.main div[data-testid="stPopover"]:first-of-type { right: 4.5rem !important; top: .3rem !important; }
}
div[data-testid="stAudioInput"] {min-width:0!important;}
div[data-testid="stAudioInput"] button {border-radius:999px!important;}
.vox-composer-anchor {height:0;}
div[data-testid="stTextInput"] input {min-height:48px;border-radius:999px!important;}
div[data-testid="stAudioInput"] {padding-top:0!important;}
div[data-testid="stButton"] button[kind="primary"] {min-height:42px;width:100%;padding:0 .8rem!important;}
.vox-composer [data-testid="stTextInput"] input {min-height:50px!important;border-radius:999px!important;padding-left:18px!important;}
.vox-composer [data-testid="stPopover"] button {height:50px!important;width:50px!important;min-height:50px!important;border-radius:50%!important;padding:0!important;font-size:20px!important;}
.vox-composer [data-testid="stButton"] button {height:50px!important;min-height:50px!important;}
.vox-composer [data-testid="stHorizontalBlock"] {align-items:center!important;gap:.45rem!important;}
.vox-composer [data-testid="stTextInput"] {margin-bottom:0!important;}
[data-testid="stExpander"] {border:1px solid #2c2e43!important;border-radius:14px!important;background:rgba(18,19,30,.65)!important;}
[data-testid="stAlert"] {border-radius:12px;}
.stCaption, small {color:var(--muted)!important;}
hr {border-color:#292b40!important;}
@media (max-width: 800px) {
  .block-container {padding:2.4rem .8rem 1.2rem!important;}
  .vox-welcome {padding:8vh 0 14px;}
  .vox-welcome p {font-size:14px;margin-bottom:22px;}
  [data-testid="stChatMessage"] {padding:12px!important;}
  .stButton > button {min-height:42px;font-size:13px;}
}
</style>
""", unsafe_allow_html=True)

if "messages" not in st.session_state:
    st.session_state.messages = []
if "last_audio" not in st.session_state:
    st.session_state.last_audio = None

def queue_text_message():
    # Callbacks run before the script reruns, so widget state may safely be updated here.
    text = st.session_state.get("vox_text_entry", "").strip()
    if text:
        st.session_state["pending_prompt"] = text
        st.session_state["vox_text_entry"] = ""
    elif st.session_state.get("vox_audio_entry") is not None:
        st.session_state["pending_audio"] = True

with st.sidebar:
    st.markdown("""<div class="vox-brand"><div class="vox-logo">✦</div><div><div class="vox-title">Vox</div><div class="vox-sub">Tutor de programación</div></div></div>""", unsafe_allow_html=True)
    if st.button("＋  Nueva conversación", use_container_width=True, type="primary"):
        st.session_state.messages = []
        st.session_state.last_audio = None
        st.rerun()
    st.markdown("---")
    mode = st.selectbox("Modo", list(MODE_INSTRUCTIONS.keys()), label_visibility="visible")
    speak_answers = st.toggle("Leer respuestas en voz alta", value=True)
    voice = st.selectbox("Voz", ["alloy", "ash", "coral", "sage", "verse"], index=0)
    with st.expander("Temas para consultar"):
        for topic in ["Fundamentos", "Programación orientada a objetos", "Estructuras de datos", "Depuración", "Preparación para exámenes"]:
            st.caption("• " + topic)
    st.markdown("---")
    st.caption("Las respuestas de Vox son generadas por IA. Comprueba el código antes de usarlo.")

def send_to_vox(user_text):
    user_text = user_text.strip()
    if not user_text:
        return
    if not api_key:
        st.error("Falta OPENAI_API_KEY. Configúrala en .streamlit/secrets.toml.")
        return
    st.session_state.messages.append({"role": "user", "content": user_text})
    conversation = [{"role": m["role"], "content": m["content"]} for m in st.session_state.messages if m["role"] in ("user", "assistant")]
    instructions = SYSTEM_PROMPT + "\n\nModo actual: " + MODE_INSTRUCTIONS[mode]
    client = OpenAI(api_key=api_key)
    with st.spinner("Vox está pensando..."):
        response = client.responses.create(model=model, instructions=instructions, input=conversation)
        answer = response.output_text.strip() or "No pude generar una respuesta esta vez. ¿Puedes reformular la pregunta?"
    audio_bytes = None
    if speak_answers:
        try:
            with st.spinner("Preparando audio..."):
                speech = client.audio.speech.create(model=tts_model, voice=voice, input=answer[:4000], response_format="mp3")
                audio_bytes = speech.content
        except Exception as audio_error:
            st.info(f"La respuesta escrita está lista; no se pudo generar audio: {audio_error}")
    st.session_state.messages.append({"role": "assistant", "content": answer, "audio": audio_bytes})
    st.rerun()

# El CSS posiciona el primer popover principal en la zona superior.
with st.popover("Acerca de", help="Información sobre Vox"):
    st.markdown("### Acerca de Vox")
    st.write("Vox es un tutor de programación que explica conceptos, revisa código y ayuda a estudiar.")
    st.caption(f"Modelo de texto: {model}")
    st.caption("Las respuestas son generadas por IA. Verifica el código antes de utilizarlo.")

if not st.session_state.messages:
    st.markdown("""
    <div class="vox-welcome">
      
      <h1>¿Por dónde empezamos?</h1>
      <p>Pregunta sobre programación, comparte un error o practica para tu examen.</p>
    </div>
    """, unsafe_allow_html=True)

for item in st.session_state.messages:
    avatar = "🤖" if item["role"] == "assistant" else "🙂"
    with st.chat_message(item["role"], avatar=avatar):
        st.markdown(item["content"])
        if item["role"] == "assistant" and item.get("audio"):
            st.audio(item["audio"], format="audio/mp3")

# Procesar acciones encoladas por callbacks, antes de dibujar widgets.
pending_audio = st.session_state.pop("pending_audio", False)
pending = st.session_state.pop("pending_prompt", None)

if pending_audio and not pending:
    audio_recording = st.session_state.get("vox_audio_entry")
    if audio_recording is not None:
        try:
            if not api_key:
                st.error("Falta OPENAI_API_KEY. Configúrala en .streamlit/secrets.toml.")
            else:
                client = OpenAI(api_key=api_key)
                with st.spinner("Vox está transcribiendo tu pregunta..."):
                    transcription = client.audio.transcriptions.create(
                        model=transcription_model,
                        file=("pregunta.wav", audio_recording.getvalue(), "audio/wav"),
                        language="es"
                    )
                pending = transcription.text.strip()
                if not pending:
                    st.warning("No se detectó texto claro. Intenta grabar de nuevo.")
        except Exception as error:
            st.error(f"No se pudo procesar el audio. Detalle: {error}")

if pending:
    try:
        send_to_vox(pending)
    except Exception as error:
        st.error(f"No se pudo completar la consulta. Revisa la conexión, la clave y el saldo de API. Detalle: {error}")

# Barra de entrada compacta inspirada en interfaces conversacionales modernas.
# Enter envía el texto; el micrófono abre un control de grabación sin ocupar permanentemente la barra.
st.markdown('<div class="vox-composer-anchor"></div>', unsafe_allow_html=True)
with st.container():
    st.markdown('<div class="vox-composer">', unsafe_allow_html=True)
    plus_col, text_col, mic_col, send_col = st.columns([0.55, 8.2, 0.75, 0.8], gap="small", vertical_alignment="center")
    with plus_col:
        st.button("＋", help="Opciones de entrada", key="vox_plus", use_container_width=True,
                  on_click=lambda: st.session_state.update(show_input_help=not st.session_state.get("show_input_help", False)))
    with text_col:
        st.text_input(
            "Mensaje",
            placeholder="Pregunta a Vox…",
            label_visibility="collapsed",
            key="vox_text_entry",
            on_change=queue_text_message
        )
    with mic_col:
        with st.popover("🎙", help="Hablar con Vox", use_container_width=True):
            st.caption("Graba tu pregunta y después pulsa enviar.")
            st.audio_input("Grabar pregunta", sample_rate=16000, label_visibility="collapsed", key="vox_audio_entry")
            if st.button("Enviar audio", key="vox_send_audio", type="primary", use_container_width=True):
                st.session_state["pending_audio"] = True
                st.rerun()
    with send_col:
        st.button("↑", type="primary", use_container_width=True, help="Enviar mensaje", on_click=queue_text_message)
    st.markdown('</div>', unsafe_allow_html=True)
    if st.session_state.get("show_input_help", False):
        st.caption("Escribe tu pregunta y presiona Enter, usa la flecha para enviarla o abre el micrófono para grabar.")
