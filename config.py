import os
import sys

# ---------------------------
# Configuration
# ---------------------------

# Load API key from 'api.txt'
try:
    with open("api.txt", "r", encoding="utf-8") as file:
        API_KEY = file.read().strip()
except FileNotFoundError:
    print("Error: 'api.txt' file not found. Ensure it contains your API key.")
    sys.exit(1)

HEADERS = {
    "Authorization": f"Bearer {API_KEY}",  # Ensure 'api.txt' contains your API key
    "Content-Type": "application/json"
}

CONFIG = {
    "BASE_URL": "https://api.deepseek.com",
    "API_VERSION": "/v1/",
    "MODEL_NAME": "deepseek-chat",
    "TEMPERATURE": 0.8,
    "CHUNK_SIZE": 20000,    # How many characters per chunk when splitting text (characters)
    "GENERATION_WINDOW": 8064,  # The generation window for the model
    "REQUEST_TIMEOUT": 90,  # Timeout for the requests calls (seconds)
    "OUTPUT_DIR": "outputs"  # Where to save JSON memory files
}

from urllib.parse import urljoin

OLLAMA_URL = urljoin(CONFIG['BASE_URL'], CONFIG['API_VERSION'])
