import streamlit as st # New import for Streamlit
import google.generativeai as genai
import os
import io # New import for handling file content in memory
from dotenv import load_dotenv
from pypdf import PdfReader

# --- Configuration ---
load_dotenv()

API_KEY = os.getenv("GOOGLE_API_KEY")

if not API_KEY:
    st.error("GOOGLE_API_KEY not found in environment variables. Please set it in a .env file.")
    st.stop() # Stop the app if API key is missing

genai.configure(api_key=API_KEY)
MODEL = genai.GenerativeModel("gemini-2.0-flash")

# --- Define Folders (Not directly used in UI, but good for context) ---
JUDGMENTS_FOLDER = "judgments" # The UI will handle uploads, not read from this directly
OUTPUT_FOLDER = "output" # We won't save files to disk in this UI version for simplicity

# --- PDF Text Extraction Function (Modified for Streamlit's UploadedFile) ---
def extract_text_from_pdf(uploaded_file):
    """
    Extracts text from a Streamlit uploaded PDF file.
    Assumes the PDF contains searchable text.
    """
    text = ""
    try:
        # PdfReader can read directly from a file-like object (BytesIO)
        pdf_reader = PdfReader(io.BytesIO(uploaded_file.read()))
        for page in pdf_reader.pages:
            text += page.extract_text() or ""
        st.success(f"Successfully extracted text from: {uploaded_file.name}")
    except Exception as e:
        st.error(f"Error extracting text from {uploaded_file.name}: {e}")
        st.warning("This might happen if the PDF is scanned (image-based) and not searchable text.")
        text = "" # Return empty string on error
    return text


# --- Gemini API Function for Summarization ---
def summarize_judgment(text):
    """
    Uses the Gemini API to summarize the extracted judgment text for a law student.
    """
    if not text:
        return "No text to summarize."

    prompt = f"""
    This document may be a truncated version of a long Indian Supreme Court judgment.
    Prioritize extracting the most critical legal arguments, reasoning, and the final decision
    from the available text.

    Summarize the following Indian Supreme Court judgment for a law student.
    Focus on:
    1.  A concise overview of the case (parties, subject).
    2.  The key facts relevant to the legal issue.
    3.  The main legal issue(s) before the court.
    4.  The court's primary legal reasoning (ratio decidendi) that led to its decision.
    5.  Concurring or dissenting opinions by any judges, if applicable. (Note that this only happens when there is a three or more judge bench).
    6.  The final decision/holding.
    7.  Any important legal principles or statutes applied.

    Keep the summary clear, educational, and no longer than 250-275 words.

    Judgment Text:
    {text}
    """

    try:
        response = MODEL.generate_content(prompt)
        return response.text
    except Exception as e:
        return f"Error summarizing text: {e}"


# --- Gemini API Function for Key Information Extraction ---
def extract_key_info(text):
    """
    Uses the Gemini API to extract key information from the judgment text
    in a structured format for a law student's case brief.
    """
    if not text:
        return "No text provided for key information extraction."

    prompt = f"""
    This document may be a truncated version of a long Indian Supreme Court judgment.
    Prioritize extracting the most critical legal information from the available text.

    Extract the following specific information from the Indian Supreme Court judgment below.
    Present the output clearly, using the headings provided. If a piece of information is not found,
    state "Not found" for that specific field.

    **Case Name:**
    [Extract full case name, e.g., 'Appellant Name vs. Respondent Name']

    **Citation:**
    [Extract the official citation, e.g., '(YEAR) VOLUME SCC PAGE' or similar]

    **Court & Date:**
    [State 'Court Name' and the exact date of judgment delivery. e.g., 'Supreme Court of India, DD Month YYYY']

    **Judges:**
    [List the names of the judges who authored or concurred with the judgment]

    **Facts:**
    [Summarize the most relevant facts that led to the legal dispute, concise, around 40-60 words]. **Explicitly identify and label any direct evidence (e.g., eyewitness testimony, documents), circumstantial evidence (e.g., motive, opportunity, forensic clues) and other types of evidence (e.g., expert testimony, physical evidence), if present and relevant.**

    **Jurisdictional Basis**
    [State the specific legal provision or source of power that allows the court to hear the case such as articles/sections of the Constitution, specific statutes, etc.]

    **Issue(s):**
    [State the main legal question(s) the court was asked to decide]

    **Holding:**
    [State the court's final decision or ruling on the issue(s)]

    **Reasoning (Ratio Decidendi):**
    [Explain the core legal rationale and principles the court used to arrive at its holding]

    **Relevant Statutes/Principles:**
    [List any specific Indian Acts, Sections, or established legal principles cited or discussed]

    Judgment Text:
    {text}
    """

    try:
        response = MODEL.generate_content(prompt)
        return response.text
    except Exception as e:
        return f"Error extracting key info: {e}"


# --- Streamlit UI Layout ---
st.set_page_config(page_title="Legal AI Agent (MVP)", layout="centered")

st.title("⚖️ Legal AI Agent for Indian Law Students (MVP)")
st.markdown("Upload an Indian Supreme Court judgment PDF to get a summary and key case information.")

uploaded_file = st.file_uploader("Choose a PDF judgment file", type="pdf")

if uploaded_file is not None:
    file_details = {"FileName": uploaded_file.name, "FileType": uploaded_file.type, "FileSize": uploaded_file.size}
    st.write(file_details)

    # Process button
    if st.button("Process Judgment"):
        with st.spinner("Extracting text and analyzing judgment... This may take a moment."):
            extracted_text = extract_text_from_pdf(uploaded_file)

            if extracted_text:
                # Limit text length to avoid API token limits for very large judgments
                # Gemini Pro has a context window of 32K tokens (~40000 characters is a safe rough estimate)
                processed_text = extracted_text[:40000]

                st.subheader("Summary")
                summary = summarize_judgment(processed_text)
                st.write(summary)

                st.subheader("Key Information")
                key_info = extract_key_info(processed_text)
                st.markdown(key_info) # Use markdown for better formatting from AI output

            else:
                st.error("Could not process the PDF. Please try another file.")