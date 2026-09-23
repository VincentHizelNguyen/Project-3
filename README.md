# Korea Study AI Assistant

A multilingual education-support chatbot for questions about Korean universities, study-abroad services, and student visa information.

## Features

- Retrieval-augmented generation (RAG) over Markdown knowledge-base files
- Multilingual sentence embeddings for semantic retrieval
- Google Gemini API for response generation
- Gradio web interface with example questions
- Configurable model and retrieval count through environment variables

## Project structure

```text
Project-3/
├── app.py
├── requirements.txt
├── .env.example
└── knowledge-base/
    ├── company/
    ├── employees/
    ├── schools/
    └── visas/
```

## Setup on Windows

1. Create and activate a virtual environment:

   ```powershell
   py -m venv .venv
   .\.venv\Scripts\Activate.ps1
   ```

2. Install dependencies:

   ```powershell
   pip install -r requirements.txt
   ```

3. Copy `.env.example` to `.env` and add your Gemini API key:

   ```env
   GEMINI_API_KEY=your_api_key_here
   GEMINI_MODEL=gemini-3.5-flash-lite
   TOP_K=5
   ```

4. Run the application:

   ```powershell
   python app.py
   ```

## Attribution

This project is an adapted educational implementation based on the structure and subject matter of the reference project `tam1511/llmprojects/chatbot`. The interface and application configuration in this repository are maintained separately.

## Disclaimer

The knowledge base contains educational/demo information. Verify current university, visa, fee, and immigration requirements with official sources before making decisions.
