from mem0 import MemoryClient
import os
from dotenv import load_dotenv

load_dotenv()

mem0 = MemoryClient(api_key=os.getenv("MEM0_API_KEY"))

def save_fact_mem0(user_id: str, key: str, value: str):
    """Add a fact to Mem0"""
    mem0.add(
        user_id=user_id,
        messages=[{"role": "system", "content": f"{key}: {value}"}]
    )

def get_facts_mem0(user_id: str):
    """Retrieve all facts from Mem0 safely"""
    messages = mem0.get_all(user_id=user_id)
    facts = {}
    for msg in messages:
        content = msg.get("content")
        if not content:
            continue
        if ":" in content:
            k, v = content.split(":", 1)
            facts[k.strip()] = v.strip()
    return facts

def save_question_mem0(user_id: str, question: str):
    mem0.add(user_id=user_id, messages=[{"role": "user", "content": question}])

def get_questions_mem0(user_id: str, limit=5):
    messages = mem0.get_all(user_id=user_id)
    questions = []
    for m in messages:
        if m.get("role") == "user" and m.get("content"):
            questions.append(m["content"])
    return questions[-limit:]

def clear_user_memory_mem0(user_id: str):
    mem0.delete_all(user_id=user_id)
