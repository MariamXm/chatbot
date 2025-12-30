# llm_connector.py
import os
from groq import Groq
from dotenv import load_dotenv
from mem0_handler import mem0_client

load_dotenv()
GROQ_API_KEY = os.getenv("GROQ_API_KEY")
if not GROQ_API_KEY:
    raise ValueError("GROQ_API_KEY missing in .env")

client = Groq(api_key=GROQ_API_KEY)
GROQ_MODEL = "llama-3.3-70b-versatile"

def add_memory(messages, user_id="default_user"):
    try:
        mem0_client.add(messages=messages, user_id=user_id)
    except Exception as e:
        print(f"Mem0 add error: {e}")

def recall_memory(query, user_id="default_user"):
    try:
        results = mem0_client.search(
            query=query,
            filters={"user_id": user_id}
        )
        texts = [item["memory"] for item in results["results"]]
        return "\n".join(texts)
    except Exception as e:
        print(f"Mem0 search error: {e}")
        return ""

def get_response(user_id: str, user_input: str) -> str:
    # 1. Retrieve relevant past memories
    memory_text = recall_memory(user_input, user_id)
    messages = [{"role": "system", "content": f"Memory:\n{memory_text}"}] if memory_text else []
    messages.append({"role": "user", "content": user_input})

    # 2. Call Groq API
    try:
        completion = client.chat.completions.create(
            messages=messages,
            model=GROQ_MODEL,
            temperature=0.2
        )
        assistant_message = completion.choices[0].message.content

        # 3. Save conversation to Mem0
        add_memory([
            {"role": "user", "content": user_input},
            {"role": "assistant", "content": assistant_message}
        ], user_id=user_id)

        return assistant_message

    except Exception as e:
        return f"Groq API Error: {e}"
