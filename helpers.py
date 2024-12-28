"""
Wrapper module that re-exports utility functions from the utils package.
This maintains backward compatibility while providing a more organized structure.
"""

import os
from typing import Dict, Any, Optional, Union, List

from utils import utils
from utils.text_processing import split_text_with_overlap, process_large_file
from utils.file_io import (
    load_prompt_from_file,
    save_json_to_file,
    save_memory_to_file
)
from utils.api import call_ollama, extract_json_from_llm_output
from config import CONFIG

@utils
def process_input(input_source: str) -> List[str]:
    """
    Reads input from a text file if the input_source is a file path,
    otherwise treats the input_source as raw text.
    Uses semantic chunking with overlap to maintain context between chunks.
    
    Args:
        input_source (str): Either a file path or raw text to process
    
    Returns:
        list: A list of text chunks with overlap for context preservation
    
    Raises:
        ValueError: If the file size exceeds the maximum allowed size
    """
    if os.path.isfile(input_source):
        try:
            file_size = os.path.getsize(input_source)
            print(f"Processing file of size: {file_size / (1024*1024):.2f} MB")
            
            if file_size > CONFIG["MAX_FILE_SIZE"]:
                raise ValueError(
                    f"File size ({file_size / (1024*1024):.2f} MB) exceeds maximum allowed size "
                    f"({CONFIG['MAX_FILE_SIZE'] / (1024*1024):.2f} MB)"
                )
            
            if file_size > CONFIG["LARGE_FILE_THRESHOLD"]:
                print("Large file detected. Using streaming mode...")
                return process_large_file(input_source, CONFIG["BUFFER_SIZE"])
            
            with open(input_source, "r", encoding="utf-8") as file:
                input_text = file.read()
                
        except IOError as e:
            print(f"Error reading input file: {e}")
            return []
    else:
        input_text = input_source
        if len(input_text) > CONFIG["LARGE_FILE_THRESHOLD"]:
            print("Warning: Very large text input. Processing may take a while...")

    if not input_text:
        return []

    print("Starting text chunking...")
    return split_text_with_overlap(
        text=input_text,
        chunk_size=CONFIG["CHUNK_SIZE"],
        overlap=CONFIG["CHUNK_OVERLAP"]
    )
