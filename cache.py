from upstash_redis import Redis
import os
from dotenv import load_dotenv
import json
load_dotenv()
redis=Redis(url=os.getenv("UPSTASH_REDIS_REST_URL"), token=os.getenv("UPSTASH_REDIS_REST_TOKEN"))

def get_from_cache(question:str) -> dict:
    cached = redis.get(question)
    if cached:
        return json.loads(cached)
    return None

def save_to_cache(question:str, data:dict):
    redis.set(question, json.dumps(data), ex=3600)
