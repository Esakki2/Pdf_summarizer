import streamlit as st
from pypdf import PdfReader
import google.generativeai as genai
import os
from dotenv import load_dotenv

# ------------------- Load API Key Securely -------------------
load_dotenv()
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

genai.configure(api_key=GEMINI_API_KEY)

# ------------------- PDF Text Extraction -------------------
def extract_text_from_pdf(pdf_file):
    reader = PdfReader(pdf_file)
    text = ""
    for page in reader.pages:
        text += page.extract_text() or ""
    return text

# ------------------- Summarization using Gemini -------------------
def summarize_with_gemini(text):
    model = genai.GenerativeModel("gemini-1.5-pro")
 # ✅ Correct way
 # ✅ Correct model path

    # Keep the prompt concise and under token limit (~8000 chars is safe)
    prompt = f"Summarize the following PDF content in 3-5 bullet points:\n\n{text[:8000]}"
    
    response = model.generate_content(prompt)
    return response.text

# ------------------- Streamlit App -------------------
def main():
    st.set_page_config(page_title="PDF SUMMARIZER", page_icon="📄")
    
    st.image("log.png", width=100)  # Optional: Ensure log.png exists or comment this out
    st.title("PDF Summarizing App")
    st.markdown("Summarizing your PDF files in just a few seconds 🚀")
    st.divider()

    pdf = st.file_uploader("📄 Upload your PDF Document", type="pdf")
    submit = st.button("✨ Generate Summary")

    if submit and pdf is not None:
        with st.spinner("⏳ Extracting text and generating summary..."):
            try:
                text = extract_text_from_pdf(pdf)
                summary = summarize_with_gemini(text)
                st.subheader("📋 Summary:")
                st.write(summary)
                
                # Optional: Download button
                st.download_button("💾 Download Summary", summary, file_name="summary.txt")

            except Exception as e:
                st.error(f"❌ Error: {e}")
    elif submit:
        st.warning("⚠️ Please upload a PDF file before clicking Generate Summary.")

if __name__ == "__main__":
    main()
