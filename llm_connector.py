import os
from dotenv import load_dotenv
from groq import Groq

from memory_handler import save_fact_json, get_facts_json, save_question_json, get_questions_json
from mem0_handler import save_fact_mem0, get_facts_mem0, save_question_mem0, get_questions_mem0

GROQ_API_KEY = os.getenv("GROQ_API_KEY")
if not GROQ_API_KEY:
    raise RuntimeError("GROQ_API_KEY not set")

# client = Groq(api_key=os.getenv("GROQ_API_KEY"))
MODEL = "llama-3.3-70b-versatile"

def extract_facts(text):
    t = text.lower()
    facts = {}

    if "i like" in t:
        facts["like"] = text.split("i like", 1)[1].strip()

    if "my name is" in t:
        facts["name"] = text.split("my name is", 1)[1].strip()

    if "i am" in t and "years old" in t:
        facts["age"] = t.split("i am", 1)[1].split("years")[0].strip()

    return facts

def get_response(user_id: str, user_input: str) -> str:
    # ---------- 1️⃣ Extract & save facts ----------
    facts = extract_facts(user_input)
    for k, v in facts.items():
        save_fact_json(user_id, k, v)
        save_fact_mem0(user_id, k, v)

    # ---------- 2️⃣ Save user question ----------
    save_question_json(user_id, user_input)
    save_question_mem0(user_id, user_input)

    # ---------- 3️⃣ Load facts & questions ----------
    facts_json = get_facts_json(user_id)
    facts_mem0 = get_facts_mem0(user_id)
    all_facts = {**facts_json, **facts_mem0}  # Mem0 overwrites JSON if duplicate

    questions_json = get_questions_json(user_id)
    questions_mem0 = get_questions_mem0(user_id)
    all_questions = list(dict.fromkeys(questions_mem0 + questions_json))

    # Remove the current question from previous questions
    previous_questions = [q for q in all_questions if q != user_input][-5:]

    # ---------- 4️⃣ Build LLM messages ----------
    messages = [{"role": "system", "content": "You are a friendly assistant."}]
    
    if all_facts:
        mem_text = "Known user facts:\n" + "\n".join([f"- {k}: {v}" for k, v in all_facts.items()])
        messages.append({"role": "system", "content": mem_text})

    if previous_questions:
        hist_text = "Previously asked questions:\n" + "\n".join(previous_questions)
        messages.append({"role": "system", "content": hist_text})

    messages.append({"role": "user", "content": user_input})

    # ---------- 5️⃣ Call LLM ----------
    completion = client.chat.completions.create(
        model=MODEL,
        temperature=0.3,
        messages=messages,
    )

    return completion.choices[0].message.content
