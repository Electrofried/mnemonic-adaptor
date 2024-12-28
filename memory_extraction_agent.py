import json
from helpers import (
    call_ollama, 
    extract_json_from_llm_output
)

# Load prompts from a static JSON file at the module level
try:
    with open("prompts.json", "r") as file:
        PROMPTS = json.load(file)
        if "mem_system_prompt" not in PROMPTS or "mem_user_prompt_template" not in PROMPTS:
            raise ValueError("JSON file must contain 'system_prompt' and 'user_prompt_template'.")
except (FileNotFoundError, IOError, ValueError) as e:
    print(f"Error loading static prompts from JSON file: {e}")
    PROMPTS = {}

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

    if not PROMPTS:
        print("Static prompts are not available. Ensure 'prompts.json' is correctly configured.")
        return {}

    system_prompt = PROMPTS.get("mem_system_prompt", "")
    user_prompt_template = PROMPTS.get("mem_user_prompt_template", "")

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

    tags = memory_update.get("tags", [])
    
    # Check if there are fewer than 3 tags
    if len(tags) < 3:
        # Log the file with insufficient tags
        with open('memory_validation_errors.log', 'a') as error_log:
            error_log.write(f"ERROR_TYPE: insufficient_tags, FILE: {memory_update.get('source', 'unknown')}, TAG_COUNT: {len(tags)}, TAGS: {tags}\n")
    
    memory_update["tags"] = tags

    return {
        "type": memory_update.get("type", "memory_update"),
        "memory": memory_update.get("memory", ""),
        "context": memory_update.get("context", ""),
        "tags": memory_update.get("tags", [])
    }
