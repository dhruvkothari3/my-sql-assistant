from fastapi import FastAPI

from database import get_schema, get_join_hints, run_query, is_safe_query, clean_sql
from llm import generate_sql
from cache import get_from_cache, save_to_cache
app = FastAPI()



@app.get("/ask")
def ask(question: str):
    print(f"\n{'='*50}")
    print(f"STEP 1 - Question received: {question}")
    cached_response = get_from_cache(question)
    if cached_response:
        print(f"STEP 2 - Cache hit: Returning cached response")
        print(f"{'='*50}\n")
        return cached_response
    
    schema = get_schema()
    joins = get_join_hints()
    print(f"STEP 2 - Schema loaded: {len(schema)} characters")
    
    sql = generate_sql(question, schema, joins)
    sql = clean_sql(sql)
    print(f"STEP 3 - SQL generated: {sql}")
    
    safe, reason = is_safe_query(sql)
    print(f"STEP 4 - Safety check: {'PASSED' if safe else 'BLOCKED - ' + reason}")
    
    if not safe:
        return {
            "question": question,
            "sql_generated": sql,
            "error": f"Query blocked: {reason}",
            "results": []
        }
    
    try:
        results = run_query(sql)
        print(f"STEP 5 - Query executed: {len(results)} rows returned")
        print(f"STEP 6 - Returning results")
        print(f"{'='*50}\n")
        result = {
            "question": question,
            "sql_generated": sql,
            "results": results
        }
        save_to_cache(question, result)  # save first
        return result                     # then return
        
    except Exception as e:
        print(f"STEP 5 - Query failed: {str(e)}")
        return {
            "question": question,
            "sql_generated": sql,
            "error": f"Query failed: {str(e)}",
            "results": []
        }
    
@app.get("/clear-cache")
def clear_cache():
    from cache import redis
    redis.flushdb()
    return {"message": "Cache cleared"}
        