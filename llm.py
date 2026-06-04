from groq import Groq
import os
from dotenv import load_dotenv

load_dotenv()

client = Groq(api_key=os.getenv("GROQ_API_KEY"))

def ask_llm(prompt: str) -> str:
    response = client.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=[{"role": "user", "content": prompt}]
    )
    return response.choices[0].message.content

def generate_sql(question: str, schema: str) -> str:
    """
    Takes a natural language question + the database schema,
    returns a SQL query string.
    """
    prompt = f"""You are a SQL expert. Given the database schema below,
write a SQL query to answer the question. Return ONLY the SQL query,
no explanation, no markdown, no backticks.

Schema:
{schema}

Question: {question}

SQL Query:"""

    return ask_llm(prompt)