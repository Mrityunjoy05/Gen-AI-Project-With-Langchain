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
                # Classify query
                # from core.query_classifier import QueryClassifier
                # classifier = QueryClassifier()
                # query_type = classifier.classify(prompt)
                
                # # Show query type
                # if query_type == "document":
                #     st.info("📄 Document-based query detected")
                #     use_web_search = False
                # elif query_type == "web":
                #     st.info("🌐 Web search query detected")
                #     use_web_search = True
                # else:
                #     st.info("🔀 Hybrid query detected - using both sources")
                #     use_web_search = True
                
                # Get response
                if use_mmr:
                    response_gen = chat.get_mmr_response(prompt, use_web_search)
                    sources = chat.get_sources_mmr(prompt, use_web_search)
                else:
                    response_gen = chat.get_response(prompt, use_web_search)
                    sources = chat.get_sources(prompt, use_web_search)
                
                # Stream response
                response = st.write_stream(response_gen)
                
            
                tab1, tab2, tab3 = st.tabs(["📄 Answer", "📚 Document Evidence", "🌐 Web Evidence"])
                
                with tab1:
                    st.markdown("**Answer:**")
                    st.write(response)
                
                with tab2:
                    st.markdown("**Document Sources:**")
                    doc_sources = [s for s in sources if "Web" not in s]
                    if doc_sources:
                        for source in doc_sources:
                            st.markdown(f"📄 **{source}**")
                        
                        # Get document summaries
                        summaries = chat.rag_chain.get_document_summaries(prompt, k=3)
                        if summaries.get("summaries"):
                            st.markdown("**Document Summaries:**")
                            for summary in summaries["summaries"]:
                                with st.expander(f"📋 {summary['source']} (Rank #{summary['rank']})"):
                                    st.write(summary['summary'])
                                    st.caption(f"Relevance: {summary['relevance_score']}")
                    else:
                        st.info("No document sources used")
                
                with tab3:
                    st.markdown("**Web Sources:**")
                    web_sources = [s for s in sources if "Web" in s]
                    if web_sources:
                        for source in web_sources:
                            st.markdown(f"🌐 **{source}**")
                    else:
                        st.info("No web sources used")
                
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
                response = st.write_stream(chat.get_general_response(prompt))
                add_message("assistant", response)
                
            except Exception as e:
                error_msg = f"❌ Error: {str(e)}"
                st.error(error_msg)
                add_message("assistant", error_msg)


if __name__ == "__main__":
    main()