from fastapi import FastAPI
from llm import ask_llm

app = FastAPI()

@app.get("/test")
def test():
    response = ask_llm("Say hello and confirm you are working.")
    return {"response": response}