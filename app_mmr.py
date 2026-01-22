
import streamlit as st

# Import UI components
from ui.components import (
    init_session_state,
    display_chat_history,
    add_message,
    display_sidebar_info,
    display_file_uploader,
    display_processing_status,
    create_web_search_toggle,
    create_web_search_toggle_mmr
)
from ui.chat_interface import ChatInterface

# Page configuration
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
    
    # Initialize chat interface (cached in session state)
    if "chat_interface" not in st.session_state:
        try:
            st.session_state.chat_interface = ChatInterface()
        except Exception as e:
            st.error(f"❌ Failed to initialize chat interface: {str(e)}")
            st.stop()
    
    chat = st.session_state.chat_interface
    
    # Display sidebar
    display_sidebar_info()

    # Main content area
    st.title("🤖 AI Advocate RAG Chatbot")
    st.markdown("Chat with your documents using AI!")
    
    # File upload section
    # with st.expander("📤 Upload Documents") :#, expanded=not st.session_state.vector_store_initialized):
    #     uploaded_files = display_file_uploader()
    with st.expander("📤 Upload Documents", expanded= not st.session_state.vector_store_initialized):
        uploaded_files = display_file_uploader()

        if uploaded_files:
            # Process button
            if st.button("🚀 Process Documents", type="primary"):
                with st.spinner("Processing documents..."):
                    try:
                        num_chunks = chat.process_uploaded_files(uploaded_files)
                        # ✅ CRITICAL: Initialize RAG chain after processing
                        # chat.initialize_rag_chain()

                        display_processing_status(
                            f"✅ Processed {len(uploaded_files)} file(s) into {num_chunks} chunks!",
                            "success"
                        )
                    except Exception as e:
                        display_processing_status(f"❌ Error: {str(e)}", "error")

    # Web search toggle
    # Use it
    use_web_search, use_mmr = create_web_search_toggle_mmr()
    
    st.divider()
    
    # Display chat history
    display_chat_history()

    # Chat input
    if prompt := st.chat_input("Ask a question about your documents..."):
        # Add user message
        add_message("user", prompt)
        
        # Display user message
        with st.chat_message("user"):
            st.markdown(prompt)
        
        # Generate and display assistant response
        with st.chat_message("assistant"):
            try:
                # Choose method based on MMR
                if use_mmr:
                    response_gen = chat.get_mmr_response(prompt, use_web_search)
                    sources = chat.get_sources_mmr(prompt, use_web_search)
                else:
                    response_gen = chat.get_response(prompt, use_web_search)
                    sources = chat.get_sources(prompt, use_web_search)
                
                # Stream response
                response = st.write_stream(response_gen)

                
                # Show sources if available
                if sources:
                    with st.expander("📚 Sources"):
                        for source in sources:
                            # Different icons for different source types
                            if "Web" in source:
                                st.markdown(f"🌐 **{source}**")
                            else:
                                st.markdown(f"📄 **{source}**")
                
                # Add assistant message to history
                add_message("assistant", response, sources)
            except Exception as e:
                error_msg = f"❌ Error generating response: {str(e)}"
                st.error(error_msg)
                add_message("assistant", error_msg)
if __name__ == "__main__":
    main()