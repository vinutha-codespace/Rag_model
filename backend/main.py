from fastapi import FastAPI
from backend import search

app = FastAPI(title="HR Chatbot")

app.include_router(search.router)

# Run with: uvicorn backend.main:app --reload
