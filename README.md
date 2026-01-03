# MacroMind

AI-assisted calorie tracking platform with user-controlled predictions

## Overview
MacroMind is a full-stack backend-focused application that helps users log meals, track calorie intake, and analyze daily and weekly consumption using a hybrid ML + rule-based prediction system.

The project is designed to mirror real-world production systems, emphasizing clean APIs, data integrity, and scalable architecture.

## Key Features
- 🔐 JWT-based authentication (signup, login, protected routes)
- 🍽️ Smart meal logging with AI calorie prediction
- ✍️ User override support for correcting predicted calories
- 📅 Daily & weekly calorie summaries
- 🎯 Deficit / surplus analysis against personalized goals
- 📊 Streamlit UI for interactive usage
- 🧠 Hybrid calorie prediction (rule-based + ML regression)

backend/
├── auth/ # JWT, password hashing
├── routers/ # Users, meals, predict, stats
├── services/ # ML logic, food parsing
├── models.py # SQLAlchemy models
└── main.py # App entrypoint

macromind_ui/
├── app.py # Streamlit entrypoint
├── api.py # Backend API wrappers
├── components.py # UI components
└── config.py

## Tech Stack
**Backend**
- FastAPI
- SQLAlchemy ORM
- PostgreSQL
- JWT Authentication
- Pydantic

**ML / Data**
- Rule-based food parsing
- Linear Regression calorie estimation
- JSON-based normalized food storage

**Frontend**
- Streamlit
- REST API integration


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


## Sample Workflow
1. User signs up and sets daily calorie goal
2. Logs meals using natural language (e.g. "2 idlis and dosa")
3. System predicts calories using hybrid logic
4. User optionally overrides predicted calories
5. Meals are persisted and reflected in daily/weekly summaries

## Why This Project
This project demonstrates:
- Backend system design & API modeling
- Secure authentication workflows
- Data modeling for real-world use cases
- ML integration into production APIs
- Clean separation of concerns

## Future Enhancements
- Model retraining with user feedback
- Food image recognition
- Mobile-first frontend
- Caching & performance optimization
- CI/CD and containerization

---

## Author
**Madhu**  
Software Development Engineer (Python, Backend, Cloud)

