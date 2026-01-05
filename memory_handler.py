import json
import os

DB_FILE = "memory.json"

def _load():
    if not os.path.exists(DB_FILE):
        return {}
    with open(DB_FILE, "r") as f:
        return json.load(f)

def _save(data):
    with open(DB_FILE, "w") as f:
        json.dump(data, f, indent=2)

# ---------- FACT MEMORY ----------
def save_fact_json(user_id: str, key: str, value: str):
    """Save a fact in local JSON"""
    data = _load()
    data.setdefault(user_id, {})
    data[user_id].setdefault("facts", {})
    data[user_id]["facts"][key] = value
    _save(data)

def get_facts_json(user_id: str):
    """Get facts from JSON"""
    data = _load()
    return data.get(user_id, {}).get("facts", {})

# ---------- QUESTION MEMORY ----------
def save_question_json(user_id: str, question: str, limit=5):
    data = _load()
    data.setdefault(user_id, {})
    data[user_id].setdefault("questions", [])
    data[user_id]["questions"].append(question)
    data[user_id]["questions"] = data[user_id]["questions"][-limit:]
    _save(data)

def get_questions_json(user_id: str):
    data = _load()
    return data.get(user_id, {}).get("questions", [])

# ---------- CLEAR MEMORY ----------
def clear_user_memory_json(user_id: str):
    data = _load()
    if user_id in data:
        del data[user_id]
        _save(data)
