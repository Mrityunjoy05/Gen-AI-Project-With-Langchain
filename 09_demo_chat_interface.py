from ui.chat_interface import ChatInterface 
import ui.components  as uc
import streamlit as st

def main():

    question = "Tell me about Rohit’s journey through domestic cricket"
    uc.init_session_state()

    chat = ChatInterface()

    files = uc.display_file_uploader()
    if files :
        chat.process_uploaded_files(files)

        response = chat.get_response(query= question , use_web_search= True )

        with st.chat_message("ai"):

            st.write_stream(
                    messages for messages in response
                )
        print("Program execution finished")


if __name__ == "__main__":
    main()



