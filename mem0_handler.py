# mem0_handler.py
import os
from dotenv import load_dotenv
from mem0 import MemoryClient

load_dotenv()

MEM0_API_KEY = os.getenv("MEM0_API_KEY")
if not MEM0_API_KEY:
    raise ValueError("MEM0_API_KEY missing in .env")

mem0_client = MemoryClient(api_key=MEM0_API_KEY)
