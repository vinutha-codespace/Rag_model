import json
from sentence_transformers import SentenceTransformer
import numpy as np
import faiss

model = SentenceTransformer('all-MiniLM-L6-v2')

def load_employees(file_path='backend/employee_data.json'):
    with open(file_path, 'r') as f:
        data = json.load(f)['employees']
    return data

def build_index(employees):
    docs = []
    for emp in employees:
        text = f"{emp['name']} has {emp['experience_years']} years of experience in {', '.join(emp['skills'])} and worked on {', '.join(emp['projects'])}"
        docs.append(text)
    embeddings = model.encode(docs, convert_to_numpy=True)
    index = faiss.IndexFlatL2(embeddings.shape[1])
    index.add(embeddings)
    return index, embeddings, docs

def get_top_matches(query, employees, index, docs, k=2):
    query_embedding = model.encode([query])
    _, indices = index.search(query_embedding, k)
    return [employees[i] for i in indices[0]]
