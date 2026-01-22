
import streamlit as st

# Import UI components
from ui.components import (
    init_session_state,
    display_chat_history,
    add_message,
    display_sidebar_info,
    display_file_uploader,
    display_processing_status,
    create_web_search_toggle
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
        st.session_state.chat_interface = ChatInterface()
    
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
                        display_processing_status(
                            f"✅ Processed {len(uploaded_files)} file(s) into {num_chunks} chunks!",
                            "success"
                        )
                    except Exception as e:
                        display_processing_status(f"❌ Error: {str(e)}", "error")

    # Web search toggle
    use_web_search = create_web_search_toggle()
    
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
                # Stream the response
                response = st.write_stream(
                    chat.get_response(prompt, use_web_search=use_web_search)
                )

                # Get sources
                sources = chat.get_sources(prompt, use_web_search=use_web_search)
                
                # Show sources if available
                if sources:
                    with st.expander("📚 Sources"):
                        for source in sources:
                            st.write(f"- {source}")
                
                # Add assistant message to history
                add_message("assistant", response, sources)
            except Exception as e:
                error_msg = f"❌ Error generating response: {str(e)}"
                st.error(error_msg)
                add_message("assistant", error_msg)
if __name__ == "__main__":
    main()