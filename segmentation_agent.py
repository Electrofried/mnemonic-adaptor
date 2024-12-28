import json
from typing import List, Optional
import logging
from logging_config import get_logger
from helpers import call_ollama, extract_json_from_llm_output
from config import CONFIG

logger = get_logger(__name__)

# Load static prompts from a JSON file at the module level
try:
    with open("prompts.json", "r", encoding="utf-8") as file:
        PROMPTS = json.load(file)
        required_keys = ["seg_system_prompt", "seg_user_prompt_template"]
        if not all(key in PROMPTS for key in required_keys):
            raise ValueError(f"JSON file must contain {required_keys}")
except (FileNotFoundError, IOError, ValueError) as e:
    logger.error(f"Error loading static prompts from JSON file: {e}")
    PROMPTS = {}

def segment_input_into_chunks(input_text: str) -> Optional[List[str]]:
    """
    Requests a segmentation from the LLM that identifies only the most
    important or memorable pieces of the input. We expect a JSON list of
    strings, e.g., ["core_memory: Some text...", ...].
    """

    if not input_text:
        logger.error("Empty input text received.")
        return []

    if not PROMPTS:
        logger.error("Static prompts are not available. Ensure 'prompts.json' is correctly configured.")
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

    logger.debug(f"Raw segmentation output:\n{raw_segmentation}")

    # Attempt to parse JSON via our helper
    segmentation_response = extract_json_from_llm_output(raw_segmentation)
    if segmentation_response is None:
        logger.error("Segmentation LLM output did not contain valid JSON. Returning [].")
        return []

    if not isinstance(segmentation_response, list):
        logger.error("Segmentation did not return a JSON list. Unexpected format.")
        return []
    return segmentation_response

logger.info(f"Using model: {CONFIG.model_name}")
logger.info(f"Temperature: {CONFIG.temperature}")
