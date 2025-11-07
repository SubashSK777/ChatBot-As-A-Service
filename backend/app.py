from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
import mysql.connector
from langchain_ollama import OllamaLLM
import os

app = FastAPI()

# CORS allow all (so Streamlit can access backend)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Init LLM (Ollama mistral model)
ollama_url = os.getenv("OLLAMA_URL", "http://ollama:11434")
llm = OllamaLLM(model="mistral", base_url=ollama_url)

@app.get("/")
def root():
    return {"status": "Backend working!"}

@app.post("/ask")
async def ask_crm(request: Request):
    body = await request.json()
    prompt = body.get("prompt", "")

    response = llm.invoke(prompt)
    return {"response": response}
