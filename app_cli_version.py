import sys
import google.generativeai as genai
import os
from dotenv import load_dotenv
from pypdf import PdfReader # New import for PDF handling

# --- Configuration ---
load_dotenv() # Load environment variables from .env file

API_KEY = os.getenv("GOOGLE_API_KEY")

if not API_KEY:
    raise ValueError("GOOGLE_API_KEY not found in environment variables. Please set it in a .env file.")

genai.configure(api_key=API_KEY)
MODEL = genai.GenerativeModel('gemini-2.0-flash') # Using 'gemini-2.0-flash' for text generation

# --- Define Folders ---
JUDGMENTS_FOLDER = "judgments"
OUTPUT_FOLDER = "output" # New folder for results

# --- Ensure output folder exists ---
if not os.path.exists(OUTPUT_FOLDER):
    os.makedirs(OUTPUT_FOLDER)

# --- PDF Text Extraction Function ---
def extract_text_from_pdf(pdf_path):
    """
    Extracts text from a given PDF file.
    Assumes the PDF contains searchable text.
    """
    text = ""
    try:
        reader = PdfReader(pdf_path)
        for page in reader.pages:
            text += page.extract_text() or "" # Use .extract_text() and handle potential None
        print(f"Successfully extracted text from: {os.path.basename(pdf_path)}")
    except Exception as e:
        print(f"Error extracting text from {pdf_path}: {e}")
        print("This might happen if the PDF is scanned (image-based) and not searchable text.")
        text = "" # Return empty string on error
    return text

# --- Gemini API Function for Summarization ---
def summarize_judgment(text):
    """
    Uses the Gemini API to summarize the extracted judgment text for a law student.
    """
    if not text:
        return "No text to summarize."

    # This is your prompt for summarization. We'll refine it as needed.
    prompt = f"""
    Summarize the following Indian Supreme Court judgment for a law student.
    Focus on:
    1.  A concise overview of the case (parties, subject).
    2.  The key facts relevant to the legal issue.
    3.  The main legal issue(s) before the court.
    4.  The court's primary legal reasoning (ratio decidendi) that led to its decision.
    5.  Concurring or dissenting opinions by any judges, if applicable. (Note that this only happens when there is a three or more judge bench).
    6.  The final decision/holding.
    7.  Any important legal principles or statutes applied.

    Keep the summary clear, educational, and no longer than 250-300 words.

    Judgment Text:
    {text}
    """

    try:
        response = MODEL.generate_content(prompt)
        return response.text
    except Exception as e:
        return f"Error summarizing text: {e}"
    
def extract_key_info(text):
    """
    Uses the Gemini API to extract key information from the judgment text
    in a structured format for a law student's case brief.
    """
    if not text:
        return "No text provided for key information extraction."

    prompt = f"""
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
    [Summarize the most relevant facts that led to the legal dispute, concise, around 40-60 words]

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

# --- Helper Function to Save Output ---
def save_output_to_file(filename, content):
    """Saves content to a text file in the OUTPUT_FOLDER."""
    filepath = os.path.join(OUTPUT_FOLDER, filename)
    with open(filepath, "w", encoding="utf-8") as f:
        f.write(content)
    print(f"Output saved to: {filepath}")


# --- Main Execution Block (with output saving) ---
if __name__ == "__main__":
    print("Gemini API configured successfully and model loaded!")

    # Check if a specific PDF file was provided as a command-line argument
    if len(sys.argv) > 1:
        pdf_file_name = sys.argv[1]
        pdf_base_name = os.path.splitext(pdf_file_name)[0] # Get filename without extension
        pdf_path = os.path.join(JUDGMENTS_FOLDER, pdf_file_name)

        if not os.path.exists(pdf_path):
            print(f"Error: PDF file '{pdf_file_name}' not found in the '{JUDGMENTS_FOLDER}' folder.")
            print(f"Usage: python app.py <pdf_file_name_in_judgments_folder>")
            sys.exit(1)

        print(f"\n--- Processing requested judgment: {pdf_file_name} ---")
        extracted_text = extract_text_from_pdf(pdf_path)

        if extracted_text:
            processed_text = extracted_text[:40000] # Limit text length

            # Generate and save summary
            summary = summarize_judgment(processed_text)
            summary_filename = f"{pdf_base_name}_summary.txt"
            save_output_to_file(summary_filename, summary)

            # Generate and save key information
            key_info = extract_key_info(processed_text)
            key_info_filename = f"{pdf_base_name}_key_info.txt"
            save_output_to_file(key_info_filename, key_info)

        else:
            print(f"Could not extract text from {pdf_file_name}. Skipping processing.")

    else:
        # If no argument is provided, process all PDFs
        if not os.path.exists(JUDGMENTS_FOLDER):
            print(f"Error: The '{JUDGMENTS_FOLDER}' folder does not exist. Please create it and place your PDFs inside.")
        else:
            pdf_files = [f for f in os.listdir(JUDGMENTS_FOLDER) if f.lower().endswith(".pdf")]
            if not pdf_files:
                print(f"No PDF files found in the '{JUDGMENTS_FOLDER}' folder. Please place your sample PDFs there.")
                print(f"Usage: python app.py <pdf_file_name_in_judgments_folder>")
            else:
                print("\n--- Processing all judgments in the folder ---")
                for pdf_file in pdf_files:
                    pdf_base_name = os.path.splitext(pdf_file)[0]
                    pdf_path = os.path.join(JUDGMENTS_FOLDER, pdf_file)
                    print(f"\nProcessing: {pdf_file}")

                    extracted_text = extract_text_from_pdf(pdf_path)

                    if extracted_text:
                        processed_text = extracted_text[:40000] # Limit text length

                        # Generate and save summary
                        summary = summarize_judgment(processed_text)
                        summary_filename = f"{pdf_base_name}_summary.txt"
                        save_output_to_file(summary_filename, summary)

                        # Generate and save key information
                        key_info = extract_key_info(processed_text)
                        key_info_filename = f"{pdf_base_name}_key_info.txt"
                        save_output_to_file(key_info_filename, key_info)
                    else:
                        print(f"Could not extract text from {pdf_file}. Skipping processing.")