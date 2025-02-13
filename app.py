import streamlit as st
from query_data import query_rag
from populate_database import populate_db
from datetime import datetime

##############################################################################
# PAGE CONFIGURATION STREAMLIT
##############################################################################
st.set_page_config(
    page_title="AI Agent CB-DC-1",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)

##############################################################################
# CUSTOM CSS
##############################################################################
st.markdown("""
<style>
/* Push main content down a bit */
.block-container {
    padding-top: 4rem !important;
    padding-bottom: 0rem !important;
}

/* Main background & text color */
.main {
    background-color: #1E1E1E !important;
    color: #FFFFFF !important;
}

/* Title styling */
.stTitle {
    color: #FFFFFF;
    font-size: 2.5rem !important;
    text-align: center;
    padding-bottom: 1rem;
}

/* Hide the Streamlit default toolbar */
div[data-testid="stToolbar"] {
    display: none !important;
}

/* Chat container: leave space at bottom for pinned input */
.chat-container {
    margin-bottom: 6rem; 
}

/* Assistant message bubble */
.assistant-bubble {
    background-color: #2D2D2D;
    padding: 1rem;
    border-radius: 8px;
    margin: 1rem 0;
    border: 1px solid #3D3D3D;
}

/* User message bubble */
.user-bubble {
    background-color: #007ACC;
    padding: 1rem;
    border-radius: 8px;
    margin: 1rem 0;
    border: 1px solid #005A9E;
    text-align: right;
}

/* Fixed ChatGPT-like input container at bottom */
.chatgpt-input-container {
    position: fixed;
    bottom: 0;
    left: 18rem; /* Adjust if sidebar is narrower/wider */
    right: 0;
    background-color: #343541; /* ChatGPT-like dark gray */
    border-top: 1px solid #3D3D3D;
    padding: 1rem;
    z-index: 9999; /* ensure it stays on top */
}

/* Remove extra padding inside columns */
.chatgpt-text-col > div, .chatgpt-button-col > div {
    padding: 0 !important;
    margin: 0 !important;
}
</style>
""", unsafe_allow_html=True)

##############################################################################
# SIDEBAR CONFIGURATION
##############################################################################
with st.sidebar:
    st.markdown("# 🤖")
    st.header("System Configuration")
    
    # Database Management Section
    st.subheader("📚 Database Management")
    data_path = st.text_input("Data Directory Path", "data")
    
    col1, col2 = st.columns(2)
    with col1:
        if st.button("🔄 Update DB"):
            with st.spinner("Processing documents..."):
                populate_db()
            st.success("Database updated!")
    
    with col2:
        if st.button("🗑️ Clear Cache"):
            st.cache_data.clear()
            st.success("Cache cleared!")
    
    st.markdown("---")
    st.markdown("### System Status")
    st.info("✅ System Online")

##############################################################################
# MAIN PAGE TITLE
##############################################################################
st.title("🤖 AI Agent CB-DC-1")

##############################################################################
# SESSION STATE INITIALIZATION
##############################################################################
if "messages" not in st.session_state:
    st.session_state.messages = []
if "my_text" not in st.session_state:
    st.session_state.my_text = ""

##############################################################################
# CALLBACK: HANDLE SEND
##############################################################################
def handle_send():
    query = st.session_state.my_text.strip()
    if query:
        # 1) Add user message
        st.session_state.messages.append({"role": "user", "content": query})
        
        # 2) Query the RAG pipeline
        with st.spinner("🤔 Thinking..."):
            response = query_rag(query)
            # Remove references if any
            if "\nSources:" in response:
                response_text = response.split("\nSources:", 1)[0]
            else:
                response_text = response
            response_text = response_text.replace("Response:", "").strip()
            
            # 3) Add assistant response
            final_answer = f"⏰ {datetime.now().strftime('%H:%M')}<br><br>{response_text}"
            st.session_state.messages.append({"role": "assistant", "content": final_answer})
    
    # 4) Clear the text area
    st.session_state.my_text = ""

##############################################################################
# DISPLAY THE CHAT (CHRONOLOGICAL ORDER)
##############################################################################
st.markdown("<div class='chat-container'>", unsafe_allow_html=True)
for msg in st.session_state.messages:
    if msg["role"] == "user":
        st.markdown(
            f"<div class='user-bubble'><strong>You:</strong><br>{msg['content']}</div>",
            unsafe_allow_html=True
        )
    else:
        st.markdown(
            f"<div class='assistant-bubble'><strong>AI Agent:</strong><br>{msg['content']}</div>",
            unsafe_allow_html=True
        )
st.markdown("</div>", unsafe_allow_html=True)

##############################################################################
# FIXED CHATGPT-STYLE INPUT AT THE BOTTOM
##############################################################################
st.markdown("<div class='chatgpt-input-container'>", unsafe_allow_html=True)

text_col, button_col = st.columns([8,1], gap="small")
with text_col:
    st.text_area(
        "Your message...",
        key="my_text",
        label_visibility="collapsed",
        placeholder="Type your question here...",
        height=70
    )
with button_col:
    st.button("Send", on_click=handle_send)

st.markdown("</div>", unsafe_allow_html=True)

##############################################################################
# FOOTER
##############################################################################
st.markdown(
    """
    <div style='text-align: center; color: #666; padding-top: 2rem;'>
        <small>AI Agent CB-DC-1 | Version 1.0 | Powered by LangChain & Ollama</small>
    </div>
    """,
    unsafe_allow_html=True
)