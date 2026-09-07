import os
from dotenv import load_dotenv

load_dotenv()

GROQ_API_KEY = os.getenv("GROQ_API_KEY")
HF_TOKEN = os.getenv("HF_TOKEN")
LLM_MODEL = os.getenv("LLM_MODEL", "qwen/qwen3.8-27b")