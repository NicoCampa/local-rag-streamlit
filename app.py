import streamlit as st
from query_data import query_rag
from populate_database import populate_db
from datetime import datetime

##############################################################################
# PAGE CONFIGURATION STREAMLIT
##############################################################################
st.set_page_config(
    page_title="AI Agent",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)

##############################################################################
# CUSTOM CSS
##############################################################################
st.markdown("""
<style>
/* Modern color scheme and variables */
:root {
    --primary-color: #2E7DAF;
    --bg-color: #1E1E2E;
    --text-color: #E0E0E0;
    --bubble-user: #2E7DAF;
    --bubble-assistant: #2D2D3D;
    --accent-color: #64B5F6;
}

/* Smooth scrolling and better animations */
@keyframes fadeIn {
    from { opacity: 0; transform: translateY(20px); }
    to { opacity: 1; transform: translateY(0); }
}

@keyframes slideIn {
    from { transform: translateX(-20px); opacity: 0; }
    to { transform: translateX(0); opacity: 1; }
}

/* Global styles */
.main {
    background: linear-gradient(135deg, var(--bg-color), #2D2D3D) !important;
    color: var(--text-color) !important;
    font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
}

.block-container {
    padding-top: 2rem !important;
    padding-bottom: 0rem !important;
    max-width: 1200px !important;
}

/* Modern title styling */
.stTitle {
    color: var(--text-color);
    font-size: 2.8rem !important;
    font-weight: 700 !important;
    text-align: center;
    padding: 1.5rem 0;
    text-shadow: 0 2px 10px rgba(0,0,0,0.3);
    letter-spacing: -0.5px;
}

/* Hide Streamlit elements */
div[data-testid="stToolbar"], footer {
    display: none !important;
}

/* Chat container with better spacing */
.chat-container {
    margin-bottom: 7rem;
    padding: 0 1rem;
}

/* Message bubbles with modern styling */
.assistant-bubble, .user-bubble {
    padding: 1.2rem;
    border-radius: 12px;
    margin: 1.5rem 0;
    box-shadow: 0 4px 15px rgba(0,0,0,0.1);
    animation: fadeIn 0.5s ease-out;
    max-width: 85%;
    line-height: 1.5;
}

.assistant-bubble {
    background-color: var(--bubble-assistant);
    border: 1px solid rgba(255,255,255,0.1);
    margin-right: auto;
    animation: slideIn 0.5s ease-out;
}

.user-bubble {
    background-color: var(--bubble-user);
    margin-left: auto;
    text-align: right;
    animation: slideIn 0.5s ease-out;
}

/* Input container with glass effect */
.chatgpt-input-container {
    position: fixed;
    bottom: 0;
    left: 18rem;
    right: 0;
    background: rgba(30, 30, 46, 0.95);
    backdrop-filter: blur(10px);
    padding: 1.2rem;
    z-index: 9999;
    border-top: 1px solid rgba(255,255,255,0.1);
    box-shadow: 0 -5px 20px rgba(0,0,0,0.2);
}

/* Textarea styling */
.stTextArea textarea {
    background-color: rgba(45, 45, 61, 0.8) !important;
    border: 1px solid rgba(255,255,255,0.1) !important;
    border-radius: 8px !important;
    color: var(--text-color) !important;
    font-size: 1rem !important;
    padding: 0.8rem !important;
    transition: all 0.3s ease;
}

.stTextArea textarea:focus {
    border-color: var(--accent-color) !important;
    box-shadow: 0 0 0 2px rgba(100, 181, 246, 0.2) !important;
}

/* Button styling */
.stButton button {
    background: var(--primary-color) !important;
    color: white !important;
    border: none !important;
    border-radius: 8px !important;
    padding: 0.5rem 1.2rem !important;
    font-weight: 500 !important;
    transition: all 0.2s ease !important;
    min-height: 40px !important;
    width: auto !important;
    font-size: 0.95rem !important;
    line-height: 1.2 !important;
    display: inline-flex !important;
    align-items: center !important;
    justify-content: center !important;
}

/* Specific styling for the send button */
.chatgpt-input-container .stButton button {
    height: 46px !important;
    width: 100px !important;
}

/* Specific styling for sidebar buttons */
.sidebar .stButton button {
    width: 100% !important;
    margin: 0.3rem 0 !important;
    height: auto !important;
    min-height: 38px !important;
    font-size: 0.9rem !important;
    background: rgba(46, 125, 175, 0.8) !important;
}

.stButton button:hover {
    background: var(--accent-color) !important;
    transform: translateY(-1px);
    box-shadow: 0 3px 8px rgba(0,0,0,0.15);
}

/* Sidebar improvements */
.css-1d391kg {
    background-color: var(--bg-color) !important;
}

.sidebar .sidebar-content {
    background: linear-gradient(180deg, var(--bg-color), #2D2D3D) !important;
}

/* Improved scrollbar */
::-webkit-scrollbar {
    width: 8px;
    height: 8px;
}

::-webkit-scrollbar-track {
    background: rgba(255,255,255,0.1);
}

::-webkit-scrollbar-thumb {
    background: rgba(255,255,255,0.2);
    border-radius: 4px;
}

::-webkit-scrollbar-thumb:hover {
    background: rgba(255,255,255,0.3);
}
</style>
""", unsafe_allow_html=True)

##############################################################################
# SIDEBAR CONFIGURATION
##############################################################################
with st.sidebar:
    st.markdown("# 🤖 AI Assistant")
    
    # Chat Settings
    st.markdown("### 💬 Chat Settings")
    
    # Temperature slider for response variety
    temperature = st.slider(
        "Response Creativity",
        min_value=0.0,
        max_value=1.0,
        value=0.7,
        help="Lower values make responses more focused and deterministic, higher values make them more creative and varied"
    )
    
    # Chat History Management
    st.markdown("### 📝 Chat History")
    if st.button("🗑️ Clear Chat History"):
        st.session_state.messages = []
        st.rerun()
    
    # Display Mode
    st.markdown("### 🎨 Display")
    theme_mode = st.selectbox(
        "Theme",
        options=["Dark", "Light"],
        index=0
    )
    
    # Quick Actions
    st.markdown("### ⚡ Quick Actions")
    quick_prompts = [
        "Summarize our conversation",   
        "Explain the last response",
        "Show me some examples",
    ]
    
    if st.button("📋 Summarize Chat"):
        summary_prompt = "Please summarize our conversation so far."
        st.session_state.my_text = summary_prompt
        handle_send()
    
    # System Status
    st.markdown("### 📊 System Status")
    st.info("✅ System Online")
    
    # Help & Information
    with st.expander("ℹ️ Help & Tips"):
        st.markdown("""
        **Tips for better results:**
        - Be specific in your questions
        - Provide context when needed
        - Use follow-up questions
        - Try different creativity levels
        """)

# Update CSS for the new sidebar elements
st.markdown("""
<style>
/* Sidebar header styling */
.sidebar .sidebar-content h1 {
    margin-bottom: 2rem;
    color: var(--text-color);
    font-size: 1.5rem !important;
}

/* Sidebar section headers */
.sidebar .sidebar-content h3 {
    margin-top: 1.5rem;
    color: var(--text-color);
    font-size: 1rem !important;
    opacity: 0.9;
}

/* Sidebar slider styling */
.sidebar .stSlider {
    margin-bottom: 1.5rem;
}

/* Sidebar button improvements */
.sidebar .stButton button {
    background: rgba(46, 125, 175, 0.1) !important;
    border: 1px solid rgba(46, 125, 175, 0.2) !important;
    color: var(--text-color) !important;
    transition: all 0.2s ease;
}

.sidebar .stButton button:hover {
    background: rgba(46, 125, 175, 0.2) !important;
    border-color: rgba(46, 125, 175, 0.3) !important;
}

/* Sidebar expander styling */
.sidebar .streamlit-expanderHeader {
    color: var(--text-color) !important;
    opacity: 0.8;
    font-size: 0.9rem !important;
}

/* Status indicator styling */
.sidebar .stAlert {
    background: rgba(25, 135, 84, 0.1) !important;
    border-color: rgba(25, 135, 84, 0.2) !important;
}

/* Select box styling */
.sidebar .stSelectbox {
    margin-bottom: 1rem;
}

.sidebar .stSelectbox > div > div {
    background: rgba(46, 125, 175, 0.1) !important;
    border-color: rgba(46, 125, 175, 0.2) !important;
}
</style>
""", unsafe_allow_html=True)

##############################################################################
# MAIN PAGE TITLE
##############################################################################
st.title("🤖 AI Agent")

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
            
            # 3) Add assistant response (without datetime)
            final_answer = response_text
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
        <small>AI Agent | Version 1.0 | Developed by Nicolò Campagnoli</small>
    </div>
    """,
    unsafe_allow_html=True
)
