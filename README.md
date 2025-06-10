# Legal AI Agent MVP for Indian Law Students

## Project Overview

This project is a Minimum Viable Product (MVP) for an AI agent designed to assist Indian law students in their legal research and case analysis. It automates the process of extracting text from PDF judgments, summarizing them, and pulling out key information for case briefing.

## Features

- **PDF Text Extraction:** Extracts searchable text from Indian Supreme Court judgment PDFs.
- **Judgment Summarization:** Generates concise, educational summaries tailored for law students, focusing on facts, issues, reasoning (ratio decidendi), and decisions.
- **Key Information Extraction:** Extracts structured data points like Case Name, Citation, Judges, Facts, Issue(s), Holding, Reasoning, and Relevant Statutes/Principles.
- **Command-Line Interface (CLI):** Allows users to process individual judgment files or all judgments in a designated folder.
- **Output Saving:** Saves generated summaries and key information to dedicated text files for easy review and record-keeping.

## Setup and Installation

1.  **Clone/Download the Project:**
    [Instructions on how to get your code, e.g., if it's in a Git repository or just copy the folder]

2.  **Install Python:**
    Ensure you have Python 3.9+ installed. Download from [python.org](https://www.python.org/downloads/).

3.  **Install Required Libraries:**
    Navigate to the project root directory (`legal_ai_mvp`) in your terminal and run:

    ```bash
    pip install google-generativeai python-dotenv pypdf
    ```

4.  **Set up Google Gemini API Key:**
    - Go to [Google AI Studio](https://aistudio.google.com/) and obtain a new API key.
    - In your `legal_ai_mvp` folder, create a file named `.env`.
    - Add your API key to this file in the following format:
      ```
      GEMINI_API_KEY="YOUR_ACTUAL_GEMINI_API_KEY_HERE"
      ```
    - **Important:** Ensure you have a `.gitignore` file with `.env` in it to prevent accidentally sharing your key.

## Usage

1.  **Place Judgment PDFs:**
    Place your Indian Supreme Court judgment PDF files into the `judgments/` subfolder.

2.  **Run the Agent:**

    - **To process a specific judgment:**

      ```bash
      python app.py <your_judgment_filename.pdf>
      ```

      (e.g., `python app.py example_case.pdf`)

    - **To process all judgments in the `judgments/` folder:**
      ```bash
      python app.py
      ```

## Output

Summaries and extracted key information will be saved as `.txt` files in the `output/` folder, named after the original PDF (e.g., `example_case_summary.txt`, `example_case_key_info.txt`).

## Future Enhancements (Beyond MVP)

- [Think of 1-2 ideas, e.g., a simple web interface, integration with legal databases, more advanced NLP for specific legal entities]

## Contact

Vidhu P Vinod
vidhupvinod@gmail.com
