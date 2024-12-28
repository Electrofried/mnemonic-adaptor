import os
import json
import requests
import uuid
import re

from config import CONFIG, HEADERS, OLLAMA_URL

def load_prompt_from_file(prompt_filename):
    """
    Loads and returns the text from the specified prompt file, or raises an exception if not found.
    """
    if not os.path.isfile(prompt_filename):
        raise FileNotFoundError(f"Prompt file not found: {prompt_filename}")
    try:
        with open(prompt_filename, "r", encoding="utf-8") as file:
            return file.read()
    except IOError as e:
        raise IOError(f"Error reading prompt file {prompt_filename}: {e}")

def save_json_to_file(data, filename):
    """
    Saves JSON data to a specified file.
    """
    try:
        with open(filename, "w", encoding="utf-8") as file:
            json.dump(data, file, indent=2, ensure_ascii=False)
        print(f"JSON data saved to {filename}")
    except IOError as e:
        print(f"Error saving JSON to {filename}: {e}")

def save_memory_to_file(memory_object, output_dir=os.path.abspath(CONFIG["OUTPUT_DIR"])):
    """
    Saves the memory object as a unique JSON file in the specified directory.
    """
    try:
        os.makedirs(output_dir, exist_ok=True)
        filename = os.path.join(output_dir, f"memory_{uuid.uuid4().hex}.json")
        with open(filename, "w", encoding="utf-8") as file:
            json.dump(memory_object, file, indent=2, ensure_ascii=False)
        print(f"Memory saved to {filename}")
    except IOError as e:
        print(f"Error saving memory to file: {e}")

def process_input(input_source):
    """
    Reads input from a text file if the input_source is a file path,
    otherwise treats the input_source as raw text.
    Splits large text (> CONFIG['CHUNK_SIZE'] characters) into smaller chunks.
    Returns a list of text chunks.
    """
    chunk_size = CONFIG["CHUNK_SIZE"]

    if os.path.isfile(input_source):
        # It's a file
        try:
            with open(input_source, "r", encoding="utf-8") as file:
                input_text = file.read()
        except IOError as e:
            print(f"Error reading input file: {e}")
            return []
    else:
        # Treat input_source as raw text
        input_text = input_source

    # Now split into chunks if needed
    if len(input_text) <= chunk_size:
        return [input_text]
    else:
        print(f"Input text exceeds {chunk_size} characters. Splitting into chunks.")
        return [
            input_text[i : i + chunk_size] 
            for i in range(0, len(input_text), chunk_size)
        ]

def call_ollama(
    user_prompt,
    system_prompt="",
    model=CONFIG["MODEL_NAME"],
    temperature=CONFIG["TEMPERATURE"]
):
    """
    Calls the Ollama API at /chat/completions with the provided user and system prompts.
    Returns the raw text response.
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
        print(f"Error calling Ollama API: {e}")
        return ""
    except (KeyError, IndexError) as e:
        print(f"Unexpected response format from Ollama: {e}")
        return ""

def extract_json_from_llm_output(llm_output):
    """
    Attempts to extract strictly valid JSON from the LLM output.
    Optionally, we look for [JSON_START] ... [JSON_END] as a sentinel.

    If there's no sentinel, we'll just do a direct json.loads on the entire string.
    Returns a Python object or None if parsing fails.
    """
    sentinel_pattern = r"\[JSON_START\](.*?)\[JSON_END\]"
    matches = re.findall(sentinel_pattern, llm_output, flags=re.DOTALL)
    if matches:
        candidate = matches[0].strip()
        try:
            return json.loads(candidate)
        except json.JSONDecodeError:
            print("Failed to parse JSON from sentinel-enclosed block.")

    # Fallback: attempt to parse entire string as JSON
    try:
        return json.loads(llm_output)
    except json.JSONDecodeError:
        print("Failed to parse JSON from entire LLM output.")
        return None
