import streamlit as st
from rag_file import ask_bot
from PIL import Image
import time

# ---------------- PAGE CONFIG ----------------
st.set_page_config(page_title="L&H FAQ BOT", page_icon="💬", layout="centered")

# ---------------- LOGO ----------------
logo = Image.open("C://Users//ss//OneDrive//Desktop//LandH//FAQ Bot//l&h_logo.png")
col1, col2, col3 = st.columns([1,2,1])
with col1: st.write("")
with col2: st.image(logo, width=140)
with col3: st.write("")

st.markdown("### Ask any question from the L&H FAQ knowledge base.")

# ---------------- SESSION STATE ----------------
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

if "last_interaction" not in st.session_state:
    st.session_state.last_interaction = time.time()

if "chat_ended" not in st.session_state:
    st.session_state.chat_ended = False

# ---------------- SIDEBAR ----------------
st.sidebar.title("Chat History")
for chat in st.session_state.chat_history:
    role = "You" if chat["role"] == "user" else "Bot"
    st.sidebar.write(f"**{role}:** {chat['message']}")

# ---------------- CONTACT BUTTON ----------------
if st.sidebar.button("Contact Support"):
    st.sidebar.info("📧 Contact us at **support@landh.com**")

# ---------------- IDLE TIMEOUT CHECK ----------------
if not st.session_state.chat_ended and time.time() - st.session_state.last_interaction > 30:
    st.warning("⏰ Chat ended due to inactivity.")
    st.session_state.chat_history.append({
        "role": "bot",
        "message": "Chat ended due to inactivity. You can refresh to start a new session."
    })
    st.session_state.chat_ended = True

# ---------------- DISPLAY CHAT ----------------
for chat in st.session_state.chat_history:
    if chat["role"] == "user":
        st.markdown(f"**You:** {chat['message']}")
    else:
        st.markdown(f"**Bot:** {chat['message']}")

# ---------------- USER INPUT ----------------
if not st.session_state.chat_ended:
    user_input = st.text_input("Type your question here:", key="user_input")

    if user_input:
        st.session_state.last_interaction = time.time()  # reset timer
        st.session_state.chat_history.append({"role": "user", "message": user_input})

        # GREETING
        if user_input.lower().strip() in ["hi", "hello", "hii", "hey"]:
            bot_reply = "Hello! 👋 How can I assist you today?"
        else:
            bot_reply = ask_bot(user_input)

        st.session_state.chat_history.append({"role": "bot", "message": bot_reply})
        st.experimental_rerun()
