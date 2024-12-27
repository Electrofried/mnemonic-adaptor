#!/usr/bin/env python3
import json
import os
import re
import requests
import sys
import uuid


# ---------------------------
# Configuration
# ---------------------------
CONFIG = {
    "BASE_URL": "http://localhost:11434",
    "API_VERSION": "/v1/",
    "MODEL_NAME": "granite3.1-moe:3b-instruct-fp16",
    "TEMPERATURE": 0.2,
    "CHUNK_SIZE": 3500,    # How many characters per chunk when splitting text (characters)
    "CONTEXT_WINDOW": 4064,  # The approximate context window for the model
    "REQUEST_TIMEOUT": 90,  # Timeout for the requests calls (seconds)
    "OUTPUT_DIR": "outputs"  # Where to save JSON memory files
}

from urllib.parse import urljoin

# You can derive this directly from the config (fewer places to update):
OLLAMA_URL = urljoin(CONFIG['BASE_URL'], CONFIG['API_VERSION'])

# ---------------------------
# Helper Functions
# ---------------------------

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

def save_memory_to_file(memory_object, output_dir=CONFIG["OUTPUT_DIR"]):
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
    Returns a list of text chunks (each up to CONFIG['CHUNK_SIZE'] characters).
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
            "num_ctx": CONFIG["CONTEXT_WINDOW"],
        },
        "stream": False,
        "raw": False
    }

    try:
        response = requests.post(
            f"{OLLAMA_URL}chat/completions",
            json=payload,
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

def segment_input_into_chunks(input_text):
    """
    Requests a segmentation from the LLM that identifies only the most
    important or memorable pieces of the input. We expect a JSON list of
    strings, e.g. ["core_memory: Some text...", ...].
    """

    # Load prompts from external files
    try:
        system_prompt = load_prompt_from_file("segmentation_agent_system_prompt.txt")
        user_prompt_template = load_prompt_from_file("segmentation_agent_user_prompt.txt")
    except (FileNotFoundError, IOError) as e:
        print(f"Error loading prompt files for segmentation: {e}")
        return []

    # Insert the input text into the user prompt
    user_prompt = user_prompt_template.replace("{INPUT_TEXT}", input_text)

    # Call the LLM
    raw_segmentation = call_ollama(
        user_prompt=user_prompt,
        system_prompt=system_prompt
    )

    # Debug
    print(f"[Debug] Raw segmentation output:\n{raw_segmentation}")

    # Attempt to parse JSON via our helper
    segmentation_response = extract_json_from_llm_output(raw_segmentation)
    if segmentation_response is None:
        print("Segmentation LLM output did not contain valid JSON. Returning [].")
        return []

    if not isinstance(segmentation_response, list):
        print("Segmentation did not return a JSON list. Unexpected format.")
        return []

    # Return the raw list of items (strings)
    return segmentation_response

def mnemonic_extraction_agent(full_chunk, core_memory_text):
    """
    Processes the data with the mnemonic agent to create a memory object
    specific to the given core memory text.

    We expect the LLM to return a JSON object of the form:
      {
        "type": "memory_update",
        "memory": "string",
        "context": "string",
        "tags": [ "keywords", "minimum", "three" ]
      }
    """

    if not full_chunk or not core_memory_text:
        print("Invalid data provided for mnemonic extraction (missing chunk or memory text).")
        return {}

    # Load prompts
    try:
        system_prompt = load_prompt_from_file("memory_extraction_agent_system_prompt.txt")
        user_prompt_template = load_prompt_from_file("memory_extraction_agent_user_prompt.txt")
    except (FileNotFoundError, IOError) as e:
        print(f"Error loading prompt files for mnemonic extraction: {e}")
        return {}

    user_prompt = (
        user_prompt_template
        .replace("{FULL_CHUNK}", json.dumps(full_chunk))
        .replace("{CORE_MEMORY_TEXT}", core_memory_text)
        
    )

    raw_response = call_ollama(
        user_prompt=user_prompt,
        system_prompt=system_prompt
    )
    if not raw_response:
        print("No response received from mnemonic extraction agent.")
        return {}

    memory_update = extract_json_from_llm_output(raw_response)
    if memory_update is None:
        print("Could not parse mnemonic extraction output as JSON.")
        return {}

    if not isinstance(memory_update, dict):
        print("Mnemonic extraction output is not a JSON object. Skipping.")
        return {}

    # Return the updated structure
    return {
        "type": memory_update.get("type", "memory_update"),
        "memory": memory_update.get("memory", ""),
        "context": memory_update.get("context", ""),
        "tags": memory_update.get("tags", [])
    }

def main():
    """
    Example usage:
        python {os.path.basename(__file__)} "Some text to parse and store"
        python {os.path.basename(__file__)} /path/to/some_file.txt
    """
    if len(sys.argv) < 2:
        script_name = os.path.basename(__file__)
        sys.exit()
        sys.exit(1)

    input_source = sys.argv[1]
    text_chunks = process_input(input_source)
    if not text_chunks:
        print("No text to process.")
        sys.exit()

    all_extracted_memories = []

    # Process each chunk
    for chunk_index, chunk in enumerate(text_chunks, start=1):
        print(f"\n--- Processing Chunk {chunk_index}/{len(text_chunks)} ---")

        # (a) Segment the chunk
        segments = segment_input_into_chunks(chunk)
        if not segments:
            print(f"No segments returned for chunk {chunk_index}. Moving on.")
            continue

        # (b) For each segment, parse out the text after "core_memory:"
        for segment_index, item_str in enumerate(segments, start=1):
            print(f"--- Processing Segment {segment_index}/{len(segments)} of Chunk {chunk_index} ---")

            prefix = "core_memory:"
            if item_str.startswith(prefix):
                memory_str = item_str[len(prefix):].strip()
            else:
                memory_str = item_str.strip()

            if not memory_str:
                print("Segment has no core memory text after prefix. Skipping.")
                continue

            # (c) Extract the memory
            extracted_memory = mnemonic_extraction_agent(
                full_chunk=chunk,
                core_memory_text=memory_str
            )

            # Collect if we have a real memory
            if extracted_memory and extracted_memory.get("memory"):
                all_extracted_memories.append(extracted_memory)
            else:
                print("No meaningful memory extracted for this segment.")

    # Save all collected memories in one go
    for memory in all_extracted_memories:
        save_memory_to_file(memory)

    print("\nDone processing all chunks.")

if __name__ == "__main__":
    main()
