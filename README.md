# Legal AI Agent MVP for Indian Law Students

## Project Overview

This project is a Minimum Viable Product (MVP) for an AI agent designed to assist Indian law students in their legal research and case analysis. It automates the process of extracting text from PDF judgments, summarizing them, and pulling out key information for case briefing, presented through a simple web interface.

## Live Demo (Deployed Application)

You can access and interact with the deployed version of this Legal AI Agent here:

**[https://law-sahayi.streamlit.app/]**

## NOTE
This application runs on Streamlit Community Cloud and uses a free api key, don't abuse it. The Google Gemini API key is securely handled as a Streamlit secret and is not exposed in the public codebase.

## Features

- **PDF Text Extraction:** Extracts searchable text from uploaded Indian Supreme Court judgment PDFs.
- **Judgment Summarization:** Generates concise, educational summaries tailored for law students, focusing on facts, issues, reasoning (ratio decidendi), and decisions.
- **Key Information Extraction:** Extracts structured data points like Case Name, Citation, Judges, Facts, Issue(s), Holding, Reasoning, and Relevant Statutes/Principles.
- **Web User Interface (UI):** A user-friendly interface built with Streamlit allows for easy file uploads and direct display of processed results.
- **Robustness:** Includes basic handling for potentially very long judgments by processing a truncated portion and notifying the user.

## Setup and Installation

1.  **Clone/Download the Project:**
    [Instructions on how to get your code, e.g., if it's in a Git repository or just copy the folder]

2.  **Install Python:**
    Ensure you have Python 3.9+ installed. Download from [python.org](https://www.python.org/downloads/).

3.  **Install Required Libraries:**
    Navigate to the project root directory (`legal_ai_mvp`) in your terminal and run:

    ```bash
    pip install -r requirements.txt
    ```

    (Make sure your `requirements.txt` file contains:

    ```
    google-generativeai
    python-dotenv
    pypdf
    streamlit
    ```

    )

4.  **Set up Google Gemini API Key:**
    - Go to [Google AI Studio](https://aistudio.google.com/) and obtain a new API key.
    - In your `legal_ai_mvp` folder, create a file named `.env`.
    - Add your API key to this file in the following format:
      ```
      GEMINI_API_KEY="YOUR_ACTUAL_GEMINI_API_KEY_HERE"
      ```
    - **Important:** Ensure you have a `.gitignore` file with `.env` in it to prevent accidentally sharing your key.

## Usage

1.  **Start the Web Application:**
    Navigate to the project root directory (`legal_ai_mvp`) in your terminal and run:

    ```bash
    streamlit run app.py
    ```

    This command will automatically open your web browser to the application (usually at `http://localhost:8501`).

2.  **Upload a Judgment:**
    In the web interface, click the "Choose a PDF judgment file" button and select an Indian Supreme Court judgment PDF.

3.  **Process and View:**
    Click the "Process Judgment" button. The summary and key information will be displayed directly on the webpage.

_(Optional: If you wish to use the previous Command-Line Interface (CLI) version, ensure you have renamed the file to `app_cli_version.py` and saved it. You can then run it from your terminal: `python app_cli_version.py <optional_judgment_filename.pdf>`. This version saves output to the `output/` folder.)_

## Future Enhancements (Beyond MVP)

- **Deployment to Streamlit Community Cloud:** Making the application accessible online for easier sharing and use.
- More sophisticated text chunking/summarization strategies for extremely long judgments.
- Adding a feature to define specific legal terms found in the judgment.
- Implementing user authentication and database to store processed judgments.
- Cross-reference Similar Cases Enhancement: Suggest similar or cited judgments using embedding-based similarity (e.g., FAISS + sentence transformers). Benefit: Enables deeper legal research and case comparison.
- Web or Plugin Integration Enhancement: Create a web app, VS Code plugin, or a browser extension where users can drag-and-drop PDFs. Benefit: Improves usability and real-world application.
- OCR and Low-quality PDF Handling Enhancement: Use OCR (Tesseract or Amazon Textract) to extract text from scanned PDFs with tables or signatures. Benefit: Increases compatibility with court-uploaded or historic PDFs

## Contact

Vidhu P Vinod
vidhupvinod@gmail.com
