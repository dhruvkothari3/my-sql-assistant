from fastapi import FastAPI
from llm import ask_llm
from database import get_schema, run_query
from llm import generate_sql

app = FastAPI()

@app.get("/test")
def test():
    response = ask_llm("Say hello and confirm you are working.")
    return {"response": response}

@app.get("/ask")
def ask(question: str):
    # step 1: get the database schema
    schema = get_schema()

    # step 2: send question + schema to LLM, get SQL back
    sql = generate_sql(question, schema)

    # step 3: run that SQL on the database
    results = run_query(sql)

    # step 4: return everything
    return {
        "question": question,
        "sql_generated": sql,
        "results": results
    }