# ⚖️ Legal AI Agent for Indian Law Students (MVP)

This project is an MVP (Minimum Viable Product) of a Legal AI Agent designed to assist Indian law students in quickly understanding and extracting key information from Supreme Court of India judgments. It leverages Google's Gemini AI to provide summaries and structured insights, making complex legal documents more accessible.

## ✨ Features

* **PDF Text Extraction:** Extracts searchable text from uploaded PDF judgments.
* **Judgment Validation:** Verifies if the uploaded PDF is likely an official Supreme Court of India judgment using AI.
* **Intelligent Document Chunking:** Handles long judgments by intelligently chunking the text (head and tail analysis) to optimize for AI API limits while preserving crucial information.
* **AI-Powered Summarization:** Generates a concise summary of the judgment's key aspects (overview, facts, legal issues, reasoning, decision, principles) tailored for law students.
* **Structured Key Information Extraction:** Extracts critical details such as Case Name, Citation, Court & Date, Judges, Facts (with evidence types), Jurisdictional Basis, Issue(s), Holding, Reasoning (Ratio Decidendi), Relevant Statutes/Principles, and Practical Implications.
* **PDF Analysis Download:** Allows users to download the generated summary and key information as a well-formatted PDF document using the ReportLab library, ensuring readability and proper text wrapping.
* **User-Friendly Interface:** Built with Streamlit for an intuitive web application experience.

## 🚀 Getting Started

Follow these steps to set up and run the Legal AI Agent locally.

### Prerequisites

* Python 3.8+
* `pip` (Python package installer)

### Installation

1.  **Clone the repository (if applicable):**
    ```bash
    git clone <your-repo-url>
    cd legal_ai_mvp
    ```
    (If not using Git, simply create a project folder and place `app.py`, `requirements.txt`, and `.env` inside it.)

2.  **Create a Virtual Environment (Recommended):**
    ```bash
    python -m venv venv
    ```

3.  **Activate the Virtual Environment:**
    * **Windows:**
        ```bash
        .\venv\Scripts\activate
        ```
    * **macOS/Linux:**
        ```bash
        source venv/bin/activate
        ```

4.  **Install Dependencies:**
    The project relies on a `requirements.txt` file. Make sure it contains:
    ```
    google-generativeai
    python-dotenv
    pypdf
    streamlit
    reportlab # For PDF generation
    ```
    Install them using pip:
    ```bash
    pip install -r requirements.txt
    ```

### Google Gemini API Setup

1.  **Get an API Key:**
    * Go to the [Google AI Studio](https://aistudio.google.com/app/apikey) and create a new API key for the Gemini API.

2.  **Create a `.env` file:**
    In the root directory of your project (where `app.py` is located), create a file named `.env` and add your API key:
    ```
    GOOGLE_API_KEY="YOUR_API_KEY_HERE"
    ```
    **Replace `"YOUR_API_KEY_HERE"` with the actual API key you obtained.**

### Running the Application

1.  **Ensure your virtual environment is activated.**
2.  **Run the Streamlit app:**
    ```bash
    streamlit run app.py
    ```

3.  **Access the Application:**
    Your default web browser should automatically open the Streamlit application. If not, open your browser and go to `http://localhost:8501`.

## 🔗 Deployed Application

You can access and use the deployed version of this Legal AI Agent directly in your web browser.

**[Click here to open the deployed app!](https://law-sahayi.streamlit.app/)**

**Note:** The performance and availability of the deployed app depend on the Streamlit Community Cloud (or your chosen hosting platform).

## 📚 How to Use

1.  **Upload a PDF:** Click the "Choose a PDF judgment file" button and select an Indian Supreme Court judgment in PDF format.
2.  **Process Judgment:** Click the "Process Judgment" button.
    * The app will first extract text and verify if it's an Indian Supreme Court judgment.
    * It will then use Google Gemini AI to summarize and extract key information.
    * For very long documents, it applies intelligent chunking to focus on relevant sections (head and tail).
3.  **View Analysis:** The summary and key information will be displayed directly in the web application.
4.  **Download PDF:** A "Download Analysis as PDF" button will appear, allowing you to save the generated content as a formatted PDF document.

## 🛠️ Technologies Used

* **Python:** Programming Language
* **Streamlit:** Web Application Framework
* **Google Gemini API:** For AI-powered summarization and information extraction
* **PyPDF2 (or pypdf):** For PDF text extraction
* **ReportLab:** For generating formatted PDF analysis documents
* **Python-Dotenv:** For managing environment variables (API keys)

## 🚧 Future Enhancements (Potential)

* **OCR Integration:** Implement OCR functionality for handling scanned (image-based) PDF judgments.
* **Direct Question Answering:** Allow users to ask specific questions about the judgment.
* **Citation Links:** Link extracted citations to legal databases (e.g., Indian Kanoon).
* **Precedent Analysis:** Identify and potentially categorize precedents set or followed.
* **User Authentication:** Secure access for multiple users.

---
