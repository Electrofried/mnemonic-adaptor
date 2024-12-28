"""
Wrapper module that re-exports utility functions from the utils package.
This maintains backward compatibility while providing a more organized structure.
"""

import os
from typing import Dict, Any, Optional, Union, List
from pathlib import Path
import logging
from logging_config import get_logger

from utils.text_processing import split_text_with_overlap, process_large_file
from utils.file_io import (
    load_prompt_from_file,
    save_json_to_file,
    save_memory_to_file
)
from utils.api import call_ollama, extract_json_from_llm_output
from config import CONFIG

logger = get_logger(__name__)

def process_input(input_source: Union[str, Path]) -> List[str]:
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
            logger.info(f"Processing file of size: {file_size / (1024*1024):.2f} MB")
            
            if file_size > CONFIG.max_file_size:
                raise ValueError(
                    f"File size ({file_size / (1024*1024):.2f} MB) exceeds maximum allowed size "
                    f"({CONFIG.max_file_size / (1024*1024):.2f} MB)"
                )
            
            if file_size > CONFIG.large_file_threshold:
                logger.info("Large file detected. Using streaming mode...")
                return process_large_file(input_source, CONFIG.buffer_size)
            
            with open(input_source, "r", encoding="utf-8") as file:
                input_text = file.read()
                
        except IOError as e:
            logger.error(f"Error reading input file: {e}")
            return []
    else:
        input_text = input_source
        if len(input_text) > CONFIG.large_file_threshold:
            logger.warning("Very large text input. Processing may take a while...")

    if not input_text:
        return []

    logger.info("Starting text chunking...")
    return split_text_with_overlap(
        text=input_text,
        chunk_size=CONFIG.chunk_size,
        overlap=CONFIG.chunk_overlap
    )
