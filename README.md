# AI SQL Assistant

A production-grade AI system that converts natural language questions 
into SQL queries and returns answers from a real database.

## Tech Stack
- **Backend:** FastAPI, Python
- **LLM:** Groq (Llama 3.1)
- **Database:** SQLite (Chinook)
- **Caching:** Redis (Upstash)
- **Frontend:** React

## Features
- Natural language to SQL conversion
- Automatic schema detection (tables, columns, foreign keys)
- SQL safety layer blocking dangerous queries
- Redis caching for instant repeated queries
- Step-by-step query visibility
- Clean error handling — no server crashes

## Architecture
User Question → Redis Cache Check → Schema Loading →
LLM SQL Generation → Safety Check → Query Execution → Response

## How to Run
1. Clone the repo
2. Install: `py -m pip install -r requirements.txt`
3. Add keys to `.env`:
GROQ_API_KEY=your_key
UPSTASH_REDIS_REST_URL=your_url
UPSTASH_REDIS_REST_TOKEN=your_token
4. Run backend: `py -m uvicorn main:app --reload`
5. Run frontend: `cd frontend && npm start`
6. Open: `http://localhost:3000`