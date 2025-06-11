import textwrap
import streamlit as st #import for Streamlit
import google.generativeai as genai
import os
import io #for handling file content in memory
from dotenv import load_dotenv
from pypdf import PdfReader
from fpdf import FPDF #import for PDF handling

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

# --- PDF Generation Function ---
def generate_pdf_output(summary_text, key_info_markdown, judgment_file_name="judgment_analysis"):
    pdf = FPDF()
    pdf.set_auto_page_break(auto=True, margin=15)
    pdf.add_page()

    # Set font for title
    pdf.set_font("Arial", "B", 16)
    pdf.cell(0, 10, "Legal Judgment Analysis", ln=True, align="C")
    pdf.set_font("Arial", "B", 12)
    pdf.cell(0, 10, f"Analysis for: {judgment_file_name.replace('.pdf', '')}", ln=True, align="C")
    pdf.ln(10)  # Line break

    # Summary Section
    pdf.set_font("Arial", "B", 12)
    pdf.cell(0, 10, "Summary", ln=True, align="L")
    pdf.set_font("Arial", "", 10)

    for line in summary_text.split('\n'):
        wrapped = textwrap.wrap(line, width=100)
        for wline in wrapped:
            pdf.multi_cell(180, 6, wline.encode('latin-1', 'replace').decode('latin-1'))
    pdf.ln(5)

    # Key Information Section
    pdf.set_font("Arial", "B", 12)
    pdf.cell(0, 10, "Key Information", ln=True, align="L")
    pdf.set_font("Arial", "", 10)

    lines = key_info_markdown.split('\n')
    for line in lines:
        if line.strip():
            wrapped = textwrap.wrap(line, width=100)
            if line.startswith('**') and line.endswith('**'):
                pdf.set_font("Arial", "B", 10)
                for wline in wrapped:
                    pdf.multi_cell(180, 6, wline.replace('**', '').encode('latin-1', 'replace').decode('latin-1'))
                pdf.set_font("Arial", "", 10)
            else:
                for wline in wrapped:
                    pdf.multi_cell(180, 6, wline.encode('latin-1', 'replace').decode('latin-1'))

    pdf_output_str = pdf.output(dest='S').encode('latin1')
    return pdf_output_str

# --- Gemini API Function for Judgment Classification ---
def is_indian_supreme_court_judgment(text):
    """
    Uses the Gemini API to determine if the given text is an Indian Supreme Court judgment.
    Returns True if it is, False otherwise.
    """
    if not text:
        return False # No text means it's not a judgment

    # Take a snippet of the text to save tokens for the classification
    # The beginning of legal documents usually contains identifying information
    text_snippet = text[:1000] # Use the first 1000 characters for classification

    prompt = f"""
    Analyze the following document text. Is this document an official judgment from the Supreme Court of India?
    Look for characteristic features like case names (e.g., "Appellant v. Respondent"), citations, names of judges, legal terminology common in Indian judgments, and the overall structure.

    Respond with ONLY "YES" if it is an Indian Supreme Court judgment, and ONLY "NO" if it is not.
    Do not add any other text, explanation, or punctuation.

    Document Text:
    {text_snippet}
    """

    try:
        response = MODEL.generate_content(prompt)
        # Clean the response to ensure robust parsing
        clean_response = response.text.strip().upper()

        if "YES" in clean_response:
            return True
        elif "NO" in clean_response:
            return False
        else:
            # Fallback for unexpected AI responses
            print(f"Unexpected AI response for judgment check: {clean_response}")
            return False # Default to false for safety if unexpected response
    except Exception as e:
        print(f"Error checking if document is judgment: {e}")
        return False # Return False on API error

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

    Keep the summary clear, educational, and no longer than 150-200 words.

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
    [Summarize the most relevant facts that led to the legal dispute, concise, around 40-50 words]. 
    **Explicitly identify and label any direct evidence (e.g., eyewitness testimony, documents), circumstantial evidence (e.g., motive, opportunity, forensic clues) and other types of evidence (e.g., expert testimony, physical evidence), if present and relevant.**

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

    **Practical Implications:** [State the real-world consequences or significance of this judgment for future cases, legal practice, or the interpretation of law, concise, around 30 words. If it sets a new precedent or significantly clarifies an existing one, state that.]
    
    Judgment Text:
    {text}
    """

    try:
        response = MODEL.generate_content(prompt)
        return response.text
    except Exception as e:
        return f"Error extracting key info: {e}"

# --- Text Chunking Function ---
def chunk_text(text, chunk_size=10000, chunk_overlap=1000):
    """
    Splits text into smaller chunks with overlap.
    Aims for chunks around chunk_size characters.
    """
    chunks = []
    start_index = 0
    while start_index < len(text):
        end_index = min(start_index + chunk_size, len(text))
        chunk = text[start_index:end_index]
        chunks.append(chunk)
        if end_index == len(text):
            break
        start_index += (chunk_size - chunk_overlap)
        # Ensure we don't start negative
        if start_index < 0:
            start_index = 0
    return chunks


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
        with st.spinner("Extracting text..."):
            extracted_text = extract_text_from_pdf(uploaded_file)

        if extracted_text:
            with st.spinner("Verifying document type..."):
                is_judgment = is_indian_supreme_court_judgment(extracted_text)

            if not is_judgment:
                st.error("This document does not appear to be an official judgment from the Supreme Court of India. Please upload a valid judgment PDF.")
                st.stop() # Stop further processing if it's not a judgment

            # --- MODIFIED Chunking Logic for Head-and-Tail Analysis ---
            all_chunks = chunk_text(extracted_text, chunk_size=10000, chunk_overlap=1000)

            # Define the strategy for selecting chunks
            MAX_CHUNKS_FOR_DEEPER_ANALYSIS = 20  # Overall limit for AI context (approx 200,000 chars)
            CHUNKS_FROM_START = 14               # How many chunks from the beginning
            CHUNKS_FROM_END = 6                  # How many chunks from the end

            # Ensure the sum of start and end chunks does not exceed the max allowed
            # This is a safety check and ensures logic works even if you change values later
            if (CHUNKS_FROM_START + CHUNKS_FROM_END) > MAX_CHUNKS_FOR_DEEPER_ANALYSIS:
                # Adjust CHUNKS_FROM_END if sum is too high, or rebalance as needed
                CHUNKS_FROM_END = MAX_CHUNKS_FOR_DEEPER_ANALYSIS - CHUNKS_FROM_START
                if CHUNKS_FROM_END < 0: CHUNKS_FROM_END = 0 # Ensure it's not negative

            processed_text_for_ai_parts = []
            description_for_warning = ""
            total_selected_chunks_count = 0

            if len(all_chunks) <= MAX_CHUNKS_FOR_DEEPER_ANALYSIS:
                # If the document is short enough to process fully (within our max limit)
                processed_text_for_ai_parts.extend(all_chunks)
                description_for_warning = f"completely in {len(all_chunks)} sections."
                total_selected_chunks_count = len(all_chunks)
            else:
                # Select chunks from the beginning
                head_chunks = all_chunks[:CHUNKS_FROM_START]
                processed_text_for_ai_parts.extend(head_chunks)
                
                # Select chunks from the end, ensuring no overlap with head_chunks
                # and not exceeding the total allowed chunks after taking from start.
                # The starting index for tail chunks should be after the head chunks.
                
                # Calculate how many tail chunks we *can* take without overlap AND staying within max_chunks
                actual_tail_chunks_to_take = min(CHUNKS_FROM_END, len(all_chunks) - CHUNKS_FROM_START)
                
                if actual_tail_chunks_to_take > 0:
                    tail_chunks = all_chunks[len(all_chunks) - actual_tail_chunks_to_take:]
                    # Ensure no exact duplicates if overlap occurs in very short documents,
                    # though with head_chunks_count and tail_chunks_count, this is minimized.
                    # For simplicity, if actual_tail_chunks_to_take starts *before* head_chunks end, it's better to concatenate distinct parts.
                    # This simple extend might have minor overlap if CHUNKS_FROM_START + CHUNKS_FROM_END > len(all_chunks) but handled by overall len(all_chunks) check.
                    
                    # More robust way to add tail chunks avoiding overlap:
                    # Find the starting index for tail chunks ensuring it's not within the head chunks
                    tail_start_idx = max(CHUNKS_FROM_START, len(all_chunks) - actual_tail_chunks_to_take)
                    processed_text_for_ai_parts.extend(all_chunks[tail_start_idx:])
                    
                    description_for_warning = (f"the first {len(head_chunks)} and last {actual_tail_chunks_to_take} sections.")
                else:
                    description_for_warning = (f"only the first {len(head_chunks)} sections.")
                
                total_selected_chunks_count = len(processed_text_for_ai_parts)


            processed_text_for_ai = "".join(processed_text_for_ai_parts)


            # --- Updated Warning/Info Messages ---
            if len(all_chunks) > total_selected_chunks_count: # This means we skipped middle parts
                st.warning(f"**Note:** This judgment is very long ({len(extracted_text):,} characters). "
                           f"The AI is processing **{description_for_warning}** " # Use the new description
                           f"({len(processed_text_for_ai):,} characters) for deep analysis. "
                           "The middle sections of the judgment are not included to optimize for API limits and focus on key parts (head & tail).")
            elif len(extracted_text) > 10000: # If it's more than one chunk but all fit (and processed completely by earlier logic)
                st.info(f"The judgment ({len(extracted_text):,} characters) was processed in {len(all_chunks)} sections for comprehensive analysis.")
            else: # For shorter judgments processed completely (single chunk)
                st.info(f"The judgment ({len(extracted_text):,} characters) was processed completely.")


            # --- Continue with existing processing using `processed_text_for_ai` ---
            with st.spinner("Analyzing judgment and generating output... This may take a moment."):
                st.subheader("Summary")
                summary = summarize_judgment(processed_text_for_ai) # Use processed_text_for_ai
                st.write(summary)

                st.subheader("Key Information")
                key_info = extract_key_info(processed_text_for_ai) # Use processed_text_for_ai
                st.markdown(key_info)

                # --- CORRECTED: Generate PDF bytes *after* AI processing and store in session_state ---

                download_file_name = uploaded_file.name.replace('.pdf', '_analysis.pdf')

                # Only generate the PDF bytes once, right after the AI processing is complete.
                # This ensures it's "on-demand" in the sense that it's not generated until
                # a judgment has been successfully processed by the AI.
                pdf_bytes_for_download = generate_pdf_output(summary, key_info, uploaded_file.name)

                # Store the generated bytes and desired file name in session state.
                # This makes them persist across Streamlit reruns.
                st.session_state['download_pdf_bytes'] = pdf_bytes_for_download
                st.session_state['download_file_name'] = download_file_name

            # --- Render the download button AFTER processing ---
            # It will retrieve the data from session_state.
            # This button will now appear only after a successful judgment processing.
            if 'download_pdf_bytes' in st.session_state:
                st.download_button(
                    label="Download Analysis as PDF",
                    data=st.session_state['download_pdf_bytes'], # Access the pre-generated bytes
                    file_name=st.session_state['download_file_name'],
                    mime="application/pdf"
                )

        else:
            st.error("Could not extract text from the PDF. Please try another file.")