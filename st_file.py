import streamlit as st
from rag_file import ask_bot
from PIL import Image

# st.set_page_config(page_title="L&H FAQ BOT", page_icon="💬", layout="centered")

# Load Logo
logo = Image.open("FAQ Bot/l&h_logo.png")

# Center logo + title
col1, col2, col3 = st.columns([1,2,1])
with col1:
    st.write("")
with col2:
    st.image(logo, width=140)
    # st.markdown(
    #     "<h2 style='text-align:left; color:#D62828; font-weight:700;'>L&H FAQ BOT</h2>",
    #     unsafe_allow_html=True
    # )
with col3:
    st.write("")

st.write("Ask any question from the L&H FAQ knowledge base.")

# No session_state → just a simple input
user_input = st.text_input("Type your question:")

if user_input:
    st.markdown(f"**You:** {user_input}")

    with st.spinner("Processing..."):
        bot_reply = ask_bot(user_input)

    st.markdown(f"**Bot:** {bot_reply}")
