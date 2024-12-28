import json
from helpers import call_ollama, extract_json_from_llm_output
from config import CONFIG
from typing import List

# Load static prompts from a JSON file at the module level
try:
    with open("prompts.json", "r", encoding="utf-8") as file:
        PROMPTS = json.load(file)
        required_keys = ["seg_system_prompt", "seg_user_prompt_template"]
        if not all(key in PROMPTS for key in required_keys):
            raise ValueError(f"JSON file must contain {required_keys}")
except (FileNotFoundError, IOError, ValueError) as e:
    print(f"Error loading static prompts from JSON file: {e}")
    PROMPTS = {}
def segment_input_into_chunks(input_text: str) -> List[str]:
    """
    Requests a segmentation from the LLM that identifies only the most
    important or memorable pieces of the input. We expect a JSON list of
    strings, e.g., ["core_memory: Some text...", ...].
    """

    if not input_text:
        print("Empty input text received.")
        return []

    if not PROMPTS:
        print("Static prompts are not available. Ensure 'prompts.json' is correctly configured.")
        return []

    # Retrieve the system and user prompts from the static JSON
    system_prompt = PROMPTS.get("seg_system_prompt", "")
    user_prompt_template = PROMPTS.get("seg_user_prompt_template", "")

    # Insert the input text into the user prompt template
    user_prompt = user_prompt_template.replace("{INPUT_TEXT}", input_text)

    # Call the LLM
    raw_segmentation = call_ollama(
        user_prompt=user_prompt,
        system_prompt=system_prompt
    )

    print(f"[Debug] Raw segmentation output:\n{raw_segmentation}")

    # Attempt to parse JSON via our helper
    segmentation_response = extract_json_from_llm_output(raw_segmentation)
    if segmentation_response is None:
        print("Segmentation LLM output did not contain valid JSON. Returning [].")
        return []

    if not isinstance(segmentation_response, list):
        print("Segmentation did not return a JSON list. Unexpected format.")
        return []
    return segmentation_response

print(f"[Config] Using model: {CONFIG['MODEL_NAME']}")
print(f"[Config] Temperature: {CONFIG['TEMPERATURE']}")
