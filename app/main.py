from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List
import json
from app.rag import RAGSystem
from app.models import QueryRequest, Employee

app = FastAPI(title="HR Resource Query Chatbot")


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


with open("data/employees.json", "r") as f:
    employee_data = json.load(f)["employees"]
rag_system = RAGSystem(employee_data)

@app.post("/chat", response_model=dict)
async def chat(query: QueryRequest):
    try:
        response = rag_system.process_query(query.text)
        return {"response": response}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/employees/search", response_model=List[Employee])
async def search_employees(query: str):
    try:
        employees = rag_system.retrieve_employees(query)
        return employees
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))