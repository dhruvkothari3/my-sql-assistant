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

def generate_sql(question: str, schema: str, joins: str) -> str:
    prompt = f"""You are a SQLite expert.

DATABASE SCHEMA:
{schema}

AVAILABLE JOINS (use these exact JOIN patterns when combining tables):
{joins}

RULES:
- Use LIMIT not TOP
- SQLite syntax only
- Always use GROUP BY when using COUNT with ORDER BY
- Use the exact JOIN patterns shown above
- Never reference a column that is not in the schema
- Always put a space before LIMIT
- To count records from another table, always JOIN that table first then count its column
- Return ONLY the raw SQL query on a single line, nothing else

Question: {question}
SQLite Query:"""

    return ask_llm(prompt)