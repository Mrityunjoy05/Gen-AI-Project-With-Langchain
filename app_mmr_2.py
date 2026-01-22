# app.py
import streamlit as st

from ui.components import (
    init_session_state,
    display_chat_history,
    add_message,
    display_sidebar_info,
    display_file_uploader,
    display_processing_status,
    create_web_search_toggle_mmr
)
from ui.chat_interface import ChatInterface

st.set_page_config(
    page_title="AI Advocate RAG Chatbot",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)


def main():
    """Main application function."""
    
    # Initialize session state
    init_session_state()
    
    # Initialize chat interface
    if "chat_interface" not in st.session_state:
        try:
            st.session_state.chat_interface = ChatInterface()
        except Exception as e:
            st.error(f"❌ Failed to initialize: {str(e)}")
            st.stop()
    
    chat = st.session_state.chat_interface
    
    # Display sidebar (includes mode switcher)
    display_sidebar_info()
    
    # ✅ Route to different UIs based on mode
    if st.session_state.chat_mode == 'rag':
        display_rag_mode(chat)
    else:
        display_general_mode(chat)


def display_rag_mode(chat):
    """Display RAG chat interface."""
    
    # Title
    st.title("🤖 AI Advocate RAG Chatbot")
    st.markdown("💬 Chat with your documents using AI!")
    
    # File upload
    with st.expander("📤 Upload Documents", expanded=not st.session_state.vector_store_initialized):
        uploaded_files = display_file_uploader()

        if uploaded_files:
            if st.button("🚀 Process Documents", type="primary"):
                with st.spinner("Processing..."):
                    try:
                        num_chunks = chat.process_uploaded_files(uploaded_files)
                        display_processing_status(
                            f"✅ Processed {len(uploaded_files)} file(s) into {num_chunks} chunks!",
                            "success"
                        )
                    except Exception as e:
                        display_processing_status(f"❌ Error: {str(e)}", "error")

    # Search options
    use_web_search, use_mmr = create_web_search_toggle_mmr()
    
    st.divider()
    
    # Chat history
    display_chat_history()

    # Chat input
    if prompt := st.chat_input("💬 Ask about your documents..."):
        add_message("user", prompt)
        
        with st.chat_message("user"):
            st.markdown(prompt)
        
        with st.chat_message("assistant"):
            try:
                if use_mmr:
                    response_gen = chat.get_mmr_response(prompt, use_web_search)
                    sources = chat.get_sources_mmr(prompt, use_web_search)
                else:
                    response_gen = chat.get_response(prompt, use_web_search)
                    sources = chat.get_sources(prompt, use_web_search)
                
                response = st.write_stream(response_gen)
                
                if sources:
                    with st.expander("📚 Sources"):
                        for source in sources:
                            if "Web" in source:
                                st.markdown(f"🌐 **{source}**")
                            else:
                                st.markdown(f"📄 **{source}**")
                
                add_message("assistant", response, sources)
                
            except Exception as e:
                error_msg = f"❌ Error: {str(e)}"
                st.error(error_msg)
                add_message("assistant", error_msg)


def display_general_mode(chat):
    """Display general chat interface."""
    
    # Title
    st.title("💬 General AI Chat")
    st.markdown("🤖 Chat with AI about anything!")
    
    # Info box
    st.info("ℹ️ This is general conversation mode. Your documents are not used here.")
    
    st.divider()
    
    # Chat history
    display_chat_history()
    
    # Chat input
    if prompt := st.chat_input("💬 Ask me anything..."):
        add_message("user", prompt)
        
        with st.chat_message("user"):
            st.markdown(prompt)
        
        with st.chat_message("assistant"):
            try:
                # ✅ Call your general chat method
                response = st.write_stream(chat.get_general_response(prompt))
                add_message("assistant", response)
                
            except Exception as e:
                error_msg = f"❌ Error: {str(e)}"
                st.error(error_msg)
                add_message("assistant", error_msg)


if __name__ == "__main__":
    main()