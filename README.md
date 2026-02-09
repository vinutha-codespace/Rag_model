HR Resource Query Chatbot
Introduction
This project is an AI-powered HR assistant chatbot designed to help HR teams find employees based on natural language queries, such as "Find Python developers with 3+ years experience" or "Who has worked on healthcare projects?" The chatbot uses a Retrieval-Augmented Generation (RAG) system to process queries and return formatted responses with matching employee profiles. It is built using Python 3.12.4, FastAPI for the backend, Streamlit for the frontend, and HuggingFace's all-MiniLM-L6-v2 model for embedding-based search. This README provides a beginner-friendly explanation of the project, including code details, setup instructions, and how it meets the assignment requirements.
Project Overview
The HR Resource Query Chatbot enables HR teams to:

Search for employees using natural language queries based on skills, experience, or past projects.
Retrieve relevant employee data using a RAG system with embedding-based search.
Access a FastAPI backend with REST endpoints (/chat and /employees/search).
Interact via a simple Streamlit chat interface.
Use a sample dataset of 15 employees stored in employees.json.

The project is located at ..\Desktop\hr_chatbot
Project Structure
The project directory (hr_chatbot) contains:

data/employees.json: Sample employee dataset.
app/main.py: FastAPI backend with API endpoints.
app/rag.py: RAG system implementation (Retrieval, Augmentation, Generation).
app/models.py: Pydantic models for data validation.
frontend/streamlit_app.py: Streamlit frontend for the chat interface.
requirements.txt: Python dependencies.
README.md: This documentation file.
hr_chatbot_documentation.tex: LaTeX source for detailed project documentation.

Code Explanation
This section explains each code file, its purpose, and key components in a beginner-friendly way.
data/employees.json
Purpose: Stores a dataset of 15 employees with attributes like id, name, skills, experience_years, projects, and availability. It serves as the data layer for the chatbot.
Key Details:

Format: JSON array of employee objects.
Example entry:{
    "id": 1,
    "name": "Alice Johnson",
    "skills": ["Python", "React", "AWS"],
    "experience_years": 5,
    "projects": ["E-commerce Platform", "Healthcare Dashboard"],
    "availability": "available"
}


Used by: app/main.py to load employee data for the RAG system.

app/main.py
Purpose: Sets up the FastAPI backend with two API endpoints: /chat (POST) for natural language queries and /employees/search (GET) for direct employee searches.
Key Code:
from fastapi import FastAPI, HTTPException
from app.rag import RAGSystem
from app.models import QueryRequest, Employee
app = FastAPI(title="HR Resource Query Chatbot")
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

Explanation:

Imports the RAGSystem and Pydantic models (QueryRequest, Employee).
Loads employees.json and initializes the RAG system.
The /chat endpoint processes queries (e.g., "Find Python developers") and returns a natural language response.
CORS middleware allows the Streamlit frontend to communicate with the backend.

app/rag.py
Purpose: Implements the RAG system, which retrieves relevant employees, augments data with query context, and generates readable responses.
Key Code:
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity
class RAGSystem:
    def __init__(self, employee_data):
        self.employees = [Employee(**emp) for emp in employee_data]
        self.model = SentenceTransformer('all-MiniLM-L6-v2')
        self.employee_embeddings = self._generate_embeddings()
    def _generate_embeddings(self):
        employee_texts = [
            f"{emp.name} has {emp.experience_years} years of experience with skills {', '.join(emp.skills)} and worked on projects: {', '.join(emp.projects)}"
            for emp in self.employees
        ]
        return self.model.encode(employee_texts)
    def process_query(self, query):
        query_embedding = self.model.encode([query])[0]
        similarities = cosine_similarity([query_embedding], self.employee_embeddings)[0]
        top_indices = np.argsort(similarities)[-3:][::-1]
        relevant_employees = [self.employees[i] for i in top_indices if similarities[i] > 0.3]
        response = f"Based on your query '{query}', I found {len(relevant_employees)} suitable candidates:\n\n"
        for emp in relevant_employees:
            response += (
                f"**{emp.name}**:\n- Experience: {emp.experience_years} years\n- Skills: {', '.join(emp.skills)}\n- Past Projects: {', '.join(emp.projects)}\n- Availability: {emp.availability.capitalize()}\n\n"
            )
        return response

Explanation:

Uses SentenceTransformer to create embeddings for employee data and queries.
retrieve_employees: Finds the top 3 employees with cosine similarity above 0.3.
process_query: Combines retrieval and generation to produce a readable response.

app/models.py
Purpose: Defines Pydantic models for validating API requests and employee data.
Key Code:
from pydantic import BaseModel
from typing import List
class QueryRequest(BaseModel):
    text: str
class Employee(BaseModel):
    id: int
    name: str
    skills: List[str]
    experience_years: int
    projects: List[str]
    availability: str

Explanation:

QueryRequest: Validates query text (e.g., "Find Python developers").
Employee: Ensures employee data from employees.json is structured correctly.

frontend/streamlit_app.py
Purpose: Creates a Streamlit frontend for an interactive chat interface.
Key Code:
import streamlit as st
import requests
st.title("HR Resource Query Chatbot")
if "messages" not in st.session_state:
    st.session_state.messages = []
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])
if prompt := st.chat_input("Enter your query"):
    with st.chat_message("user"):
        st.markdown(prompt)
    st.session_state.messages.append({"role": "user", "content": prompt})
    try:
        response = requests.post("http://localhost:8000/chat", json={"text": prompt})
        response.raise_for_status()
        result = response.json()["response"]
        with st.chat_message("assistant"):
            st.markdown(result)
        st.session_state.messages.append({"role": "assistant", "content": result})
    except requests.exceptions.RequestException as e:
        st.error(f"Error: Could not connect to backend. {str(e)}")

Explanation:

Displays a chat interface with a text input for queries.
Sends queries to the /chat endpoint and shows responses.
Maintains chat history using Streamlit’s session state.

requirements.txt
Purpose: Lists Python dependencies required for the project.
Content:
fastapi==0.115.0
uvicorn==0.30.6
sentence-transformers==2.7.0
transformers==4.39.3
numpy==1.26.4
scikit-learn==1.5.2
streamlit==1.39.0
requests==2.32.3
pydantic==2.9.2

Explanation:

Specifies exact versions to ensure compatibility with Python 3.12.4.
Uses sentence-transformers==2.7.0 to avoid issues with codecarbon.

hr_chatbot_documentation.tex
Purpose: LaTeX source file for generating a detailed PDF documentation (not required for running the project but included for reference).
Explanation:

Contains the same content as this README but formatted for PDF output.
Can be compiled with pdflatex to produce a professional document.

Setup Instructions
To run the project on Windows with Python 3.12.4:

Clone the repository:git clone https://github.com/tyagaraj-raj-2007/hr_chatbot.git
cd hr_chatbot


Create and activate a virtual environment:python -m venv venv
.\venv\Scripts\activate


Install dependencies:pip install -r requirements.txt


Run the FastAPI backend:uvicorn app.main:app --host 0.0.0.0 --port 8000


Run the Streamlit frontend (in a new terminal):.\venv\Scripts\activate
streamlit run frontend/streamlit_app.py


Access the app:
Open http://localhost:8501 in your browser for the Streamlit interface.
Test the API at http://localhost:8000/docs for Swagger documentation.



API Documentation

POST /chat
Request:{"text": "Find Python developers with 3+ years experience"}


Response: Natural language response with matching employees.
Example:{
    "response": "Based on your query 'Find Python developers with 3+ years experience', I found 3 suitable candidates:\n\n**Alice Johnson**:\n- Experience: 5 years\n- Skills: Python, React, AWS\n- Past Projects: E-commerce Platform, Healthcare Dashboard\n- Availability: Available\n\n..."
}




GET /employees/search?query=
Query param: query (e.g., "Python developers")
Response: List of matching employee objects.
Example:[
    {
        "id": 1,
        "name": "Alice Johnson",
        "skills": ["Python", "React", "AWS"],
        "experience_years": 5,
        "projects": ["E-commerce Platform", "Healthcare Dashboard"],
        "availability": "available"
    }
]





Meeting Assignment Requirements
The project fulfills the core requirements of the assignment:

Data Layer: employees.json contains 15+ employee records with required attributes.
RAG System: Implemented in rag.py with embedding-based retrieval and template-based generation.
Backend API: FastAPI endpoints in main.py with error handling and validation.
Frontend Interface: Streamlit interface in streamlit_app.py for user-friendly interaction.
Deliverables: Includes GitHub repository, working demo, README.md, and sample dataset.

AI Development Process

Tools Used:
Grok (xAI) for architecture planning and code review.
GitHub Copilot for code autocompletion.


Usage:
Grok assisted in designing the RAG pipeline and selecting technologies (FastAPI, Streamlit, SentenceTransformer).
Copilot helped write ~30% of the code (e.g., FastAPI setup, Pydantic models).


Manual Work:
Fine-tuned similarity threshold (0.3) for better retrieval relevance.
Customized response formatting for readability.


Challenges:
AI struggled with Streamlit session state management; resolved manually.
Dependency conflicts (e.g., codecarbon) were handled by downgrading sentence-transformers.



Technical Decisions

Embedding Model: Chose all-MiniLM-L6-v2 for fast, lightweight embeddings suitable for small datasets.
No External LLM: Used template-based generation to avoid API costs and ensure offline compatibility.
FastAPI: Selected for async support and automatic Swagger documentation.
Streamlit: Chosen for rapid frontend development and simplicity.
Trade-offs:
Prioritized simplicity (embedding search) over complex LLMs for faster setup.
Used local models to ensure data privacy.



Troubleshooting Tips

Port Conflict: If port 8000 is in use, run:uvicorn app.main:app --host 0.0.0.0 --port 8001

Update streamlit_app.py to use http://localhost:8001/chat.
Dependency Issues: Recreate the virtual environment and run:pip install -r requirements.txt


Test Backend: Use http://localhost:8000/docs to test API endpoints.
Test SentenceTransformer:echo "from sentence_transformers import SentenceTransformer; model = SentenceTransformer('all-MiniLM-L6-v2'); print('Model loaded successfully!')" > test.py
python test.py



GitHub Repository
The source code is available at: https://github.com/tyagaraj-raj-2007/hr_chatbot.git 
Demo

Local Demo: Run the setup instructions and access at http://localhost:8501.
Screenshots: (Add screenshots or a deployed demo link if available.)

Future Improvements

Add support for local LLMs (e.g., Ollama with Llama) for advanced responses.
Implement FAISS for faster vector search with larger datasets.
Add filters for availability and experience years in the search endpoint.
Deploy to Streamlit Cloud or Vercel for public access.
