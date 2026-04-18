# import os
# from dotenv import load_dotenv

# load_dotenv()

# GROQ_API_KEY = os.getenv("GROQ_API_KEY")
# HINDSIGHT_API_KEY = os.getenv("HINDSIGHT_API_KEY")


import os
from dotenv import load_dotenv

load_dotenv()

GROQ_API_KEY = os.getenv("GROQ_API_KEY")
HINDSIGHT_API_KEY = os.getenv("HINDSIGHT_API_KEY")

if not GROQ_API_KEY:
    raise ValueError("Missing GROQ_API_KEY in .env")

if not HINDSIGHT_API_KEY:
    raise ValueError("Missing HINDSIGHT_API_KEY in .env")