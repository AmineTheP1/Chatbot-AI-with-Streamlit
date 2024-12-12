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

    # Upload a PDF file
    pdf = st.file_uploader("Upload your PDF", type='pdf')

    if pdf is not None:
        pdf_reader = PdfReader(pdf)
        text = ""
        for page in pdf_reader.pages:
            text += page.extract_text()
        
        title = st.text_input("Enter a title for this PDF:")
        if st.button("Upload PDF"):
            if title:
                pdf_id = db_operations.upload_pdf(title, text)
                st.success(f"PDF uploaded with ID: {pdf_id}")
            else:
                st.error("Please provide a title for the PDF.")

    st.header("Ask Questions about Stored PDFs")

    pdfs = db_operations.get_all_pdfs_content()

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
                
    # Section to delete a PDF
    st.subheader("Delete a PDF")
    pdf_id_to_delete = st.selectbox("Select a PDF to delete", 
                                  [f"{pdf[0]}: {pdf[2]}" for pdf in pdfs])  # Use pdf[2] for title
    if st.button("Delete PDF"):
        if pdf_id_to_delete:
            pdf_id = int(pdf_id_to_delete.split(':')[0])
            deleted_pdf_title = db_operations.delete_pdf(pdf_id)
            st.success(f"PDF '{deleted_pdf_title}' has been deleted.")
        else:
            st.error("Please select a PDF to delete.")

if __name__ == '__main__':
    main()
