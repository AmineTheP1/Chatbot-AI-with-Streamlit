import streamlit as st
from dotenv import load_dotenv
from PyPDF2 import PdfReader
from mistralai.client import MistralClient
from mistralai.models.chat_completion import ChatMessage
import os
import db_operations

# Load environment variables from .env file
load_dotenv()

@st.cache_resource
def load_client():
    api_key = os.getenv("MISTRAL_API_KEY")
    if not api_key:
        st.error("MISTRAL_API_KEY environment variable not set. Please set it in the .env file or environment.")
        return None
    client = MistralClient(api_key=api_key)
    return client

def main():
    st.header("Chat with PDF 💬")

    st.header("Ask Questions about Stored PDFs")

    query = st.text_input("Ask a question about the PDFs:")
    if query:
        client = load_client()
        if client:
            all_pdfs_content = db_operations.get_all_pdfs_content()
            context = "\n".join([pdf[1] for pdf in all_pdfs_content])
            message = ChatMessage(
                role="user",
                content=f"Context: {context}\nQuestion: {query}"
            )
            response = client.chat(
                model="mistral-large-latest",
                messages=[message]
            )
            answer = response.choices[0].message.content
            st.write("Answer:", answer)

if __name__ == '__main__':
    main()
