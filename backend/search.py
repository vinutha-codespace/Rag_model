from fastapi import APIRouter
from backend.model_utils import load_employees, build_index, get_top_matches

router = APIRouter()

employees = load_employees()
index, embeddings, docs = build_index(employees)

@router.post("/chat")
def chat(query: str):
    results = get_top_matches(query, employees, index, docs)
    formatted = []
    for emp in results:
        profile = f"{emp['name']} has {emp['experience_years']} years of experience in {', '.join(emp['skills'])}. Projects: {', '.join(emp['projects'])}. Availability: {emp['availability']}."
        formatted.append(profile)
    return {"response": "\n\n".join(formatted)}
