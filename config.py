import os
import sys
from urllib.parse import urljoin

# Configuration section for API and system settings
# This section handles API key loading and validation

# Load API key from api.txt file with proper error handling
try:
    with open("api.txt", "r", encoding="utf-8") as file:
        API_KEY = file.read().strip()
except FileNotFoundError:
    API_KEY = os.getenv("API_KEY", "")
    if not API_KEY:
        print("Warning: No API key found. Some features may not work.")

# Validate API key format and length
# Ensures the API key meets minimum requirements before proceeding
if not API_KEY or len(API_KEY.strip()) < 10:  # adjust minimum length as needed
    print("Error: Invalid API key format in 'api.txt'")
    sys.exit(1)

# Define request headers for API calls
HEADERS = {
    "Authorization": f"Bearer {API_KEY}",
    "Content-Type": "application/json"
}

# Main configuration dictionary containing all system settings
CONFIG = {
    "BASE_URL": os.getenv("DEEPSEEK_BASE_URL", "https://api.deepseek.com"),  # Base URL with environment variable fallback
    "API_VERSION": "/v1/",                    # API version path
    "MODEL_NAME": "deepseek-chat",            # Model identifier
    "TEMPERATURE": 0.8,                       # Controls randomness in model output
    "CHUNK_SIZE": 20000,                      # Text chunk size for processing
    "CHUNK_OVERLAP": 200,                     # Overlap size between chunks for context preservation
    "GENERATION_WINDOW": 8064,                # Model's context window size
    "REQUEST_TIMEOUT": 90,                    # API request timeout in seconds
    "OUTPUT_DIR": os.path.join(os.getcwd(), "outputs"),  # Default output directory
    "LARGE_FILE_THRESHOLD": 100 * 1024 * 1024,  # Size in bytes (100MB) to trigger large file handling
    "BUFFER_SIZE": 1024 * 1024,              # Buffer size for reading large files (1MB)
    "MAX_FILE_SIZE": 1024 * 1024 * 1024,     # Maximum file size to process (1GB)
}

# Construct full API URL using urljoin for proper URL handling
OLLAMA_URL: str = urljoin(CONFIG['BASE_URL'], CONFIG['API_VERSION'])
