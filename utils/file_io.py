"""
File input/output utilities for handling prompts, JSON, and memory objects.
"""

import os
import json
import uuid
import logging
from typing import Dict, Any, Optional
from pathlib import Path
from logging_config import get_logger

logger = get_logger(__name__)

def load_prompt_from_file(prompt_filename: str) -> str:
    """
    Loads and returns the text from the specified prompt file.
    
    Args:
        prompt_filename (str): Path to the prompt file to be loaded
    
    Returns:
        str: The contents of the prompt file
        
    Raises:
        FileNotFoundError: If the prompt file doesn't exist
        IOError: If there's an error reading the file
    """
    if not os.path.isfile(prompt_filename):
        raise FileNotFoundError(f"Prompt file not found: {prompt_filename}")
    try:
        with open(prompt_filename, "r", encoding="utf-8") as file:
            return file.read()
    except IOError as e:
        raise IOError(f"Error reading prompt file {prompt_filename}: {e}")

def save_json_to_file(data: Dict[str, Any], filename: str) -> None:
    """
    Saves JSON data to a specified file.
    
    Args:
        data (dict): The JSON data to save
        filename (str): Path where the JSON file should be saved
    """
    try:
        os.makedirs(os.path.dirname(filename), exist_ok=True)
        with open(filename, "w", encoding="utf-8") as file:
            json.dump(data, file, indent=2, ensure_ascii=False)
        logger.info(f"JSON data saved to {filename}")
    except IOError as e:
        logger.error(f"Error saving JSON to {filename}: {e}")

def save_memory_to_file(memory_object: Dict[str, Any], output_dir: Optional[str] = None) -> None:
    """
    Saves the memory object as a unique JSON file in the specified directory.
    
    Args:
        memory_object (dict): The memory object to save
        output_dir (str, optional): Directory to save the file. Defaults to 'outputs' in current directory
    """
    if output_dir is None:
        output_dir = os.path.join(os.getcwd(), "outputs")
    
    try:
        os.makedirs(output_dir, exist_ok=True)
        filename = os.path.join(output_dir, f"memory_{uuid.uuid4().hex}.json")
        with open(filename, "w", encoding="utf-8") as file:
            json.dump(memory_object, file, indent=2, ensure_ascii=False)
        logger.info(f"Memory saved to {filename}")
    except IOError as e:
        logger.error(f"Error saving memory to file: {e}")
