# MacroMind

**Smart Calorie Tracking System** — an end-to-end project demonstrating Data Engineering, Machine Learning, and LLM-powered user experience.

**Repo structure**
- `backend/` — FastAPI backend (APIs, DB models, calorie lookup, parsers)
- `airflow/` — ETL / daily summary dags (Prefect/Airflow)
- `ml/` — preprocessing, training scripts, models
- `ai/` — RAG / LLM assistant integration
- `dashboard/` — Streamlit visualization app
- `docs/` — architecture diagrams, design notes

## Project summary
MacroMind is a calorie tracker which:
- accepts free-text meal logs,
- normalizes food items using a food master database,
- computes calories & macros,
- stores logs in a relational DB,
- runs daily ETL jobs for summaries,
- offers ML models for calorie estimation,
- includes an LLM assistant for conversational logging.

## Quick demo
1. Start backend: `uvicorn backend.main:app --reload`
2. Visit API docs: `http://localhost:8000/docs`
3. Start dashboard: `streamlit run dashboard/app.py`

## Tech stack
- Python, FastAPI, Pydantic
- PostgreSQL (production) / DuckDB (local)
- Apache Airflow / Prefect
- PySpark (ETL), Parquet, DuckDB
- ML: scikit-learn / transformer embeddings
- LLM & RAG: embeddings + vector DB (Chroma/Pinecone)
- Docker, GitHub Actions, AWS (S3, Lambda)

## Getting started (local)
1. Clone repo  
   `git clone https://github.com/<your-user>/MacroMind.git`
2. Create venv & install  
   ```bash
   python -m venv .venv
   source .venv/bin/activate   # linux/mac
   .venv\Scripts\activate      # windows
   pip install -r requirements.txt
