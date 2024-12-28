import json
from helpers import call_ollama, extract_json_from_llm_output

# Load static prompts from a JSON file at the module level
try:
    with open("prompts.json", "r") as file:
        PROMPTS = json.load(file)
        if "seg_system_prompt" not in PROMPTS or "seg_user_prompt_template" not in PROMPTS:
            raise ValueError("JSON file must contain 'seg_system_prompt' and 'seg_user_prompt_template'.")
except (FileNotFoundError, IOError, ValueError) as e:
    print(f"Error loading static prompts from JSON file: {e}")
    PROMPTS = {}

def segment_input_into_chunks(input_text):
    """
    Requests a segmentation from the LLM that identifies only the most
    important or memorable pieces of the input. We expect a JSON list of
    strings, e.g., ["core_memory: Some text...", ...].
    """

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
