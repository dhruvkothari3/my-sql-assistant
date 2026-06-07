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
- Only JOIN tables when the question actually requires data from multiple tables
- If the question only mentions one table, query that table directly with no JOINs
- Always SELECT meaningful columns like names, titles, totals not just IDs
- Return ONLY the raw SQL query on a single line, nothing else
- Only use LIMIT when the question asks for a specific number of results like "top 5" or "one" or "highest"
- Do not add LIMIT when the question says "all" or "show me"

EXAMPLE OF WRONG vs RIGHT:
Question: show tracks longer than 5 minutes
WRONG: SELECT * FROM Track JOIN MediaType ON Track.MediaTypeId = MediaType.MediaTypeId WHERE Milliseconds > 300000
RIGHT: SELECT * FROM Track WHERE Milliseconds > 300000

Question: which invoice has highest total
WRONG: SELECT i.InvoiceId FROM Invoice i JOIN Customer c ON i.CustomerId = c.CustomerId ORDER BY i.Total DESC LIMIT 1  
RIGHT: SELECT InvoiceId, Total FROM Invoice ORDER BY Total DESC LIMIT 1

Question: {question}
SQLite Query:"""

    return ask_llm(prompt)