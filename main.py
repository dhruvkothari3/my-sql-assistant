from fastapi import FastAPI

from database import get_schema, get_join_hints, run_query, is_safe_query
from llm import generate_sql

app = FastAPI()



@app.get("/ask")
def ask(question: str):
    schema = get_schema()
    joins = get_join_hints()
    
    # generate SQL
    sql = generate_sql(question, schema, joins)
    
    # safety check before running anything
    safe, reason = is_safe_query(sql)
    if not safe:
        return {
            "question": question,
            "sql_generated": sql,
            "error": f"Query blocked: {reason}",
            "results": []
        }
    
    # run safe query
    try:
        results = run_query(sql)
        return {
            "question": question,
            "sql_generated": sql,
            "results": results
        }
    except Exception as e:
        # catch bad SQL gracefully instead of crashing
        return {
            "question": question,
            "sql_generated": sql,
            "error": f"Query failed: {str(e)}",
            "results": []
        }
    