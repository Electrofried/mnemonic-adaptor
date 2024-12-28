"""
API interaction utilities for communicating with Ollama and handling responses.
"""

import json
import re
import time
import requests
from typing import Dict, Any, Optional, Union

from config import CONFIG, HEADERS, OLLAMA_URL
from utils import utils

@utils
def call_ollama(
    user_prompt: str,
    system_prompt: str = "",
    model: str = CONFIG["MODEL_NAME"],
    temperature: float = CONFIG["TEMPERATURE"],
    max_retries: int = 3,
    retry_delay: int = 1
) -> str:
    """
    Calls the Ollama API at /chat/completions with the provided prompts.
    Includes retry mechanism for transient failures.
    
    Args:
        user_prompt (str): The user's input prompt
        system_prompt (str, optional): System context prompt
        model (str, optional): Model to use
        temperature (float, optional): Sampling temperature
        max_retries (int, optional): Maximum number of retry attempts
        retry_delay (int, optional): Delay between retries in seconds
    
    Returns:
        str: The model's response text, or empty string if all retries fail
    """
    payload = {
        "model": model,
        "messages": [
            {"role": "system", "content": system_prompt},
            {"role": "user",   "content": user_prompt}
        ],
        "temperature": temperature,
        "options": {
            "num_ctx": CONFIG["GENERATION_WINDOW"],
        },
        "stream": False,
        "raw": False
    }

    for attempt in range(max_retries):
        try:
            response = requests.post(
                f"{OLLAMA_URL}chat/completions",
                json=payload,
                headers=HEADERS,
                timeout=CONFIG["REQUEST_TIMEOUT"]
            )
            response.raise_for_status()
            response_data = response.json()

            content = (
                response_data.get("choices", [{}])[0]
                .get("message", {})
                .get("content", "")
                .strip()
            )
            return content

        except requests.RequestException as e:
            if attempt < max_retries - 1:
                print(f"API call attempt {attempt + 1} failed: {e}. Retrying in {retry_delay} seconds...")
                time.sleep(retry_delay)
                retry_delay *= 2  # Exponential backoff
            else:
                print(f"All API call attempts failed: {e}")
                return ""
        except (KeyError, IndexError) as e:
            print(f"Unexpected response format from Ollama: {e}")
            return ""

@utils
def extract_json_from_llm_output(llm_output: str) -> Optional[Union[Dict[str, Any], list]]:
    """
    Attempts to extract strictly valid JSON from the LLM output.
    Optionally, looks for [JSON_START] ... [JSON_END] as a sentinel.
    
    Args:
        llm_output (str): Raw text output from the LLM
    
    Returns:
        dict|list|None: Parsed JSON object if successful, None if parsing fails
    """
    sentinel_pattern = r"\[JSON_START\](.*?)\[JSON_END\]"
    matches = re.findall(sentinel_pattern, llm_output, flags=re.DOTALL)
    if matches:
        candidate = matches[0].strip()
        try:
            return json.loads(candidate)
        except json.JSONDecodeError:
            print("Failed to parse JSON from sentinel-enclosed block.")

    try:
        return json.loads(llm_output)
    except json.JSONDecodeError:
        print("Failed to parse JSON from entire LLM output.")
        return None 