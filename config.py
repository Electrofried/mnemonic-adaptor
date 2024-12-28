import os
import sys
from urllib.parse import urljoin
from dataclasses import dataclass
from typing import Dict, Any

@dataclass
class Config:
    """Configuration class for the mnemonic adaptor"""
    base_url: str
    api_version: str
    model_name: str
    temperature: float
    chunk_size: int
    chunk_overlap: int
    generation_window: int
    request_timeout: int
    output_dir: str
    large_file_threshold: int
    buffer_size: int
    max_file_size: int

# Load API key from api.txt file with proper error handling
try:
    with open("api.txt", "r", encoding="utf-8") as file:
        API_KEY = file.read().strip()
except FileNotFoundError:
    API_KEY = os.getenv("API_KEY", "")
    if not API_KEY:
        print("Warning: No API key found. Some features may not work.")

# Validate API key format and length
if not API_KEY or len(API_KEY.strip()) < 10:
    print("Error: Invalid API key format in 'api.txt'")
    sys.exit(1)

# Define request headers for API calls
HEADERS = {
    "Authorization": f"Bearer {API_KEY}",
    "Content-Type": "application/json"
}

# Create configuration instance
CONFIG = Config(
    base_url=os.getenv("DEEPSEEK_BASE_URL", "https://api.deepseek.com"),
    api_version="/v1/",
    model_name="deepseek-chat",
    temperature=0.8,
    chunk_size=20000,
    chunk_overlap=200,
    generation_window=8064,
    request_timeout=90,
    output_dir=os.path.join(os.getcwd(), "outputs"),
    large_file_threshold=100 * 1024 * 1024,
    buffer_size=1024 * 1024,
    max_file_size=1024 * 1024 * 1024
)

# Construct full API URL using urljoin for proper URL handling
OLLAMA_URL: str = urljoin(CONFIG.base_url, CONFIG.api_version)

def validate_config(config: Config) -> bool:
    """Validate the configuration values"""
    required_fields = [
        'base_url', 'api_version', 'model_name', 'temperature',
        'chunk_size', 'chunk_overlap', 'generation_window',
        'request_timeout', 'output_dir', 'large_file_threshold',
        'buffer_size', 'max_file_size'
    ]
    
    for field in required_fields:
        if not getattr(config, field):
            print(f"Error: Missing required configuration field: {field}")
            return False
            
    if config.chunk_overlap >= config.chunk_size:
        print("Error: chunk_overlap must be smaller than chunk_size")
        return False
        
    if config.large_file_threshold >= config.max_file_size:
        print("Error: large_file_threshold must be smaller than max_file_size")
        return False
        
    return True

# Validate configuration on startup
if not validate_config(CONFIG):
    sys.exit(1)
