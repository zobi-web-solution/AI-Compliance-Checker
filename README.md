# ⚖️ Compliance Policy Checker

A local RAG (Retrieval-Augmented Generation) tool that checks whether a described
action or scenario complies with your company's policy documents — citing the
exact clause it relied on.

## Problem it solves

Company policy PDFs are long, and employees/managers rarely read them before acting.
This tool lets anyone type a plain-English scenario (e.g. *"Can we share employee
salary data with a vendor?"*) and get an instant, cited compliance verdict —
**COMPLIANT / NON-COMPLIANT / UNCLEAR** — backed by the actual policy text, instead
of a guess.

It runs fully locally: no data leaves the machine except to your own Qdrant
vector database.

## Tech stack

| Layer | Tool |
|---|---|
| UI | [Streamlit](https://streamlit.io) |
| Orchestration | [LangChain](https://python.langchain.com) |
| LLM | [Ollama](https://ollama.com) running `llama3.2` (local) |
| Embeddings | `all-MiniLM-L6-v2` via `langchain-huggingface` (local, free, no API key) |
| Vector store | [Qdrant](https://qdrant.io) (cloud cluster) |
| PDF parsing | PyMuPDF (`fitz`) |
| Language | Python 3.13 |

## Prerequisites

1. **Python 3.13+** with the project venv (already included at `./venv`).
2. **Ollama** installed and running, with the `llama3.2` model pulled:
   ```bash
   ollama pull llama3.2
   ```
3. **A Qdrant cluster** (cloud or self-hosted) with its URL + API key set in `.env`:
   ```
   QDRANT_URL=https://<your-cluster>.aws.cloud.qdrant.io
   QDRANT_API_KEY=<your-api-key>
   ```
4. At least one policy PDF placed in `./policies/` (currently: `Employee Policy 2026.pdf`).

> Note: `.env` also has an `OPENAI_API_KEY` entry, but nothing in the code currently
> uses it — embeddings and the LLM are both local. Safe to ignore or remove.

## Setup & run

```bash
# 1. Activate the venv (from project root)
venv\Scripts\activate

# 2. Install dependencies (only needed once, or after pulling changes)
pip install -r requirements.txt

# 3. Ingest policy PDFs into Qdrant (run once, or whenever policies/ changes)
python ingest.py

# 4. Launch the app
streamlit run app.py
```

Then open the local URL Streamlit prints (usually `http://localhost:8501`), type
a scenario, and click **Check Compliance**.

### Quick CLI test (no UI)

```bash
python checker.py
```
Runs two built-in sample scenarios and prints the verdicts to the console —
useful for confirming Ollama + Qdrant are wired up correctly before touching the UI.
