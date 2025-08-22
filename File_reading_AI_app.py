import streamlit as st
import os
from pathlib import Path
from docling.document_converter import DocumentConverter

# Streamlit App Title
st.set_page_config(page_title="Docling File Reader", layout="wide")
st.title("📂 Docling File Reader & Saver")

# Input: Destination folder path
dest_folder = st.text_input("Enter destination folder path:", "./uploaded_files")

# File uploader
uploaded_file = st.file_uploader("Upload a file", type=["pdf", "txt", "docx"])

if uploaded_file is not None and dest_folder.strip() != "":
    # Ensure destination folder exists
    Path(dest_folder).mkdir(parents=True, exist_ok=True)

    # Save uploaded file
    save_path = os.path.join(dest_folder, uploaded_file.name)
    with open(save_path, "wb") as f:
        f.write(uploaded_file.getbuffer())

    st.success(f"✅ File saved to: {save_path}")

    # --- Using Docling to read file ---
    try:
        converter = DocumentConverter()
        result = converter.convert(save_path)
        doc = result.document

        # Export content
        markdown_text = doc.export_to_markdown()

        st.subheader("📖 Extracted Content (Markdown)")
        st.markdown(markdown_text, unsafe_allow_html=True)

        # Export as structured JSON (optional)
        st.subheader("📊 Extracted Content (JSON)")
        st.json(doc.export_to_dict())

    except Exception as e:
        st.error(f"❌ Docling conversion error: {e}")

    # --- Show files in destination folder ---
    st.subheader("📂 Files in Destination Folder")
    files = os.listdir(dest_folder)
    if files:
        for f in files:
            st.write(f"- {f}")
            print(f"Files placed in the folder {files}")
    else:
        st.write("No files found in the folder yet.")
        