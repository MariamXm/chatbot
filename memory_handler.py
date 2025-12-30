# memory_handler.py
from mem0 import Mem0

# Initialize Mem0 for persistent storage (creates DB file automatically)
memory = Mem0("chatbot_memory.db")  # database file for persistence

def add_fact(user_id: str, key: str, value: str):
    """Add or update a user fact"""
    memory.set(f"{user_id}_{key}", value)

def get_fact(user_id: str, key: str):
    """Retrieve a fact for a user"""
    return memory.get(f"{user_id}_{key}")

def get_all_facts(user_id: str):
    """Retrieve all facts for a user"""
    keys = memory.keys()
    user_facts = {}
    for k in keys:
        if k.startswith(f"{user_id}_"):
            fact_key = k[len(user_id)+1:]
            user_facts[fact_key] = memory.get(k)
    return user_facts

def clear_memory(user_id: str):
    """Clear all memory for a user"""
    for k in memory.keys():
        if k.startswith(f"{user_id}_"):
            memory.delete(k)
