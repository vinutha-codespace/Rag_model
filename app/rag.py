from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np
from typing import List, Dict
from app.models import Employee

class RAGSystem:
    def __init__(self, employee_data: List[Dict]):
        self.employees = [Employee(**emp) for emp in employee_data]
        self.model = SentenceTransformer('all-MiniLM-L6-v2')
        self.employee_embeddings = self._generate_embeddings()

    def _generate_embeddings(self) -> np.ndarray:
        
        employee_texts = [
            f"{emp.name} has {emp.experience_years} years of experience with skills {', '.join(emp.skills)} "
            f"and worked on projects: {', '.join(emp.projects)}"
            for emp in self.employees
        ]
        return self.model.encode(employee_texts)

    def retrieve_employees(self, query: str) -> List[Employee]:
        query_embedding = self.model.encode([query])[0]
        similarities = cosine_similarity([query_embedding], self.employee_embeddings)[0]
        
        top_indices = np.argsort(similarities)[-3:][::-1]
        return [self.employees[i] for i in top_indices if similarities[i] > 0.3]

    def process_query(self, query: str) -> str:
        
        relevant_employees = self.retrieve_employees(query)
        
        if not relevant_employees:
            return "Sorry, I couldn't find any employees matching your requirements."

        
        response = f"Based on your query '{query}', I found {len(relevant_employees)} suitable candidates:\n\n"
        for emp in relevant_employees:
            response += (
                f"**{emp.name}**:\n"
                f"- Experience: {emp.experience_years} years\n"
                f"- Skills: {', '.join(emp.skills)}\n"
                f"- Past Projects: {', '.join(emp.projects)}\n"
                f"- Availability: {emp.availability.capitalize()}\n\n"
            )
        response += "Would you like more details about any of these candidates?"
        return response