import os 
import streamlit as st
from typing import List
import tempfile

    
def init_session_state():

    if 'messages' not in st.session_state :
        st.session_state.messages = []
        
    if 'vector_store_initialized' not in st.session_state :
        st.session_state.vector_store_initialized = False

    if 'uploaded_files' not in st.session_state :
        st.session_state.uploaded_files = []
    
    if 'chat_mode' not in st.session_state:
        st.session_state.chat_mode = 'rag'  # 'rag' or 'general'

def display_chat_history():

    for message in st.session_state.messages :
        with st.chat_message(message['role']):
            st.markdown(message['content'])

            if message.get('sources') :
                with st.expander("📚 Sources") :
                    for source in message.get('sources') :
                        st.write(f"- {source}")

def add_message(role: str, content: str, sources: List[str] = None):
    """
    Add a message to chat history.
    
    Args:
        role: 'user' or 'assistant'
        content: Message content
        sources: Optional list of source documents
    """

    message = {'role' :role ,"content" : content }

    if sources :
        message['sources'] = sources

    st.session_state.messages.append(message)

def clear_chat_history():

    st.session_state.messages = []

def save_uploaded_file(uploaded_file):

    temp_dir = tempfile.mkdtemp()

    file_path = os.path.join(temp_dir ,uploaded_file.name)

    with open(file_path , 'wb') as f:
        f.write(uploaded_file.getbuffer())
    
    return file_path


def display_sidebar_info():
    """Display information in the sidebar."""
    with st.sidebar:
        # ✅ Mode switcher at top
        display_mode_switcher()
        
        st.divider()
        
        # Rest depends on mode
        if st.session_state.chat_mode == 'rag':
            # RAG-specific sidebar
            st.header("📖 About RAG Mode")
            st.markdown("""
            **RAG (Retrieval-Augmented Generation):**
            - 📄 Answer from your documents
            - 🔍 Search the web
            - 💬 Context-aware responses
            """)
            
            st.divider()
            
            # Show uploaded files
            st.header("📁 Uploaded Files")
            if st.session_state.uploaded_files:
                for file in st.session_state.uploaded_files:
                    st.write(f"✅ {file}")
            else:
                st.write("No files uploaded yet")
        
        else:
            # General chat sidebar
            st.header("💬 About General Chat")
            st.markdown("""
            **General Conversation Mode:**
            - 🤖 Chat with AI freely
            - 💭 No document context
            - 🌟 General knowledge Q&A
            """)
        
        st.divider()
        
        # Clear chat button (common for both)
        if st.button("🗑️ Clear Chat History"):
            st.session_state.messages = []
            st.rerun()

def display_file_uploader():
    """Display file upload widget and return uploaded files."""
    uploaded_files = st.file_uploader(
        "Upload your documents (PDF or TXT)",
        type=["pdf", "txt"],
        accept_multiple_files=True,
        help="Upload documents to chat with"
    )
    return uploaded_files

def display_processing_status(message: str, status: str = "info"):
    """
    Display a status message.
    
    Args:
        message: Status message
        status: Type - 'info', 'success', 'warning', 'error'
    """
    if status == "success":
        st.success(message)
    elif status == "warning":
        st.warning(message)
    elif status == "error":
        st.error(message)
    else:
        st.info(message)

def create_web_search_toggle() -> bool:
    """Create a toggle for web search."""
    return st.toggle(
        "🌐 Enable Web Search",
        value= False,
        help="When enabled, the chatbot will also search the web for answers"
    )

def create_web_search_toggle_mmr() -> tuple[bool, bool]:
    """
    Create toggles for web search and MMR.
    
    Returns:
        tuple: (use_web_search, use_mmr)
    """
    col1, col2 = st.columns(2)
    with col1:
        use_web_search = st.toggle(
            "🌐 Enable Web Search",
            value=False,
            help="Search the web in addition to your documents"
        )
    with col2:
        use_mmr = st.toggle(
            "🔀 Diverse Results (MMR)",
            value=False,
            help="Get diverse results instead of just most similar"
        )
    
    return use_web_search, use_mmr  # ✅ Don't forget to return both!

def display_mode_switcher():
    """Display mode switcher button in sidebar."""
    
    # Current mode display
    if st.session_state.chat_mode == 'rag':
        current_mode = "📚 RAG Chat"
        switch_to = "general"
        button_text = "💬 Switch to General Chat"
        button_icon = "💬"
    else:
        current_mode = "💬 General Chat"
        switch_to = "rag"
        button_text = "📚 Switch to RAG Chat"
        button_icon = "📚"
    # Show current mode using st.html (Modern approach)
    st.html(f"""
    <div style="padding: 1rem;
                border-radius: 5px;
                text-align: center;
                margin-bottom: 1rem;">
        <h3 style="margin: 0;">{current_mode}</h3>
    </div>
""")
    # Switch button
    if st.button(button_text, use_container_width=True, type="primary"):
        st.session_state.chat_mode = switch_to
        st.session_state.messages = []
        st.rerun()

