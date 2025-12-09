import streamlit as st
from rag_file import ask_bot
from PIL import Image

# --- 1. CONFIGURATION AND INITIAL SETUP ---
# Set page configuration for a clean, wide layout
st.set_page_config(
    page_title="L&H FAQ BOT",
    page_icon="💬",
    layout="wide" 
)

# Load Logo (Assuming "FAQ Bot/l&h_logo.png" is the correct path)
try:
    # Use the logo in the sidebar for a ChatGPT-like feel
    logo = Image.open("l&h_logo.png")
except FileNotFoundError:
    logo = None

# Initialize chat history in session state
if "messages" not in st.session_state:
    st.session_state.messages = []

# --- 2. SIDEBAR (History and New Chat) ---
with st.sidebar:
    # Mimic the dark/minimalist look (often best achieved with st.set_page_config(theme='dark'))
    
    # New Chat Button at the top
    if st.button("➕ New Chat", use_container_width=True, help="Start a new conversation"):
        st.session_state.messages = []
        st.rerun()

    st.markdown("---") # Separator line
    
    # Display simplified chat history
    if st.session_state.messages:
        st.subheader("Previous Conversations")
        
        # We'll display unique conversation starters only
        conversation_titles = [m["content"][:40] + "..." for m in st.session_state.messages if m["role"] == "user"]
        
        # Display unique titles for history
        unique_titles = []
        for title in conversation_titles:
            if title not in unique_titles:
                unique_titles.append(title)
                st.caption(title) 

    # --- 3. CONTACT INFO (Placed at the bottom of the sidebar for a clean look) ---
    st.markdown("---")
    st.subheader("Contact Info")
    st.markdown(
        """
        - **Email:** support@landh.com
        - **Phone:** (555) 123-4567
        """
    )
    # Optional: Add the logo at the very bottom if desired
    if logo:
        st.image(logo, width=50)


# --- 4. MAIN INTERFACE: TITLE AND CHAT DISPLAY ---

# Keep the header minimal, centered title is often a good look
st.markdown(
    "<h1 style='text-align: center; margin-top: -50px;'>L&H FAQ BOT</h1>", 
    unsafe_allow_html=True
)

# Display a brief prompt/instruction
st.markdown(
    "<p style='text-align: center; color: gray;'>Ask any question from the L&H FAQ knowledge base.</p>", 
    unsafe_allow_html=True
)
st.markdown("<br>", unsafe_allow_html=True) # Spacer

# Display conversation history
for message in st.session_state.messages:
    # The default st.chat_message already provides the visual distinction
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# --- 5. CHAT INPUT AND RAG PROCESSING ---

# Create the input box at the bottom
if prompt := st.chat_input("Message L&H FAQ BOT..."):
    
    # 1. Store and display User message
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # 2. Get Bot response
    with st.chat_message("assistant"):
        with st.spinner("Processing your query..."):
            # Call the RAG function from rag_file
            bot_response = ask_bot(prompt)
        
        # Display Bot response
        st.markdown(bot_response)
        
    # 3. Store Bot message
    st.session_state.messages.append({"role": "assistant", "content": bot_response})
