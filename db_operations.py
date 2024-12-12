import os
import psycopg2
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

def connect_db():
    return psycopg2.connect(
        dbname=os.getenv("DB_NAME"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD"),
        host=os.getenv("DB_HOST"),
        port=os.getenv("DB_PORT")
    )

def upload_pdf(title, content):
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO pdfs (title, content) VALUES (%s, %s) RETURNING id", (title, content))
    pdf_id = cursor.fetchone()[0]
    conn.commit()
    cursor.close()
    conn.close()
    return pdf_id

def get_all_pdfs_content():
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("SELECT id, content, title FROM pdfs")
    pdfs_content = cursor.fetchall()
    cursor.close()
    conn.close()
    return pdfs_content

def delete_pdf(pdf_id):
    conn = connect_db()
    cursor = conn.cursor()

    # Fetch the title of the PDF before deleting
    cursor.execute("SELECT title FROM pdfs WHERE id = %s", (pdf_id,))
    pdf_title = cursor.fetchone()[0]

    # Delete the PDF
    cursor.execute("DELETE FROM pdfs WHERE id = %s", (pdf_id,))
    conn.commit()
    cursor.close()
    conn.close()

    return pdf_title  # Return the title of the deleted PDF

