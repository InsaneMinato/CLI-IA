import os
from dotenv import load_dotenv

load_dotenv()

MISTRAL_API_KEY = os.getenv("MISTRAL_API_KEY")
DOCUMENTS_DIR = os.getenv("DOCUMENTS_DIR", "docs/")