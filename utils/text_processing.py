"""
Text processing utilities for chunking and handling large text inputs.
"""

from typing import List
import logging
from logging_config import get_logger
from config import CONFIG

logger = get_logger(__name__)

def split_text_with_overlap(text: str, chunk_size: int = 2000, overlap: int = 200) -> List[str]:
    """
    Splits input text into overlapping chunks of specified size.
    Optimized for large files with progress feedback.
    
    Args:
        text (str): The input text to be split into chunks
        chunk_size (int): The size of each chunk in characters (default: 2000)
        overlap (int): The number of overlapping characters between chunks (default: 200)
    
    Returns:
        list: A list of text chunks with specified overlap between consecutive chunks
    """
    if not text:
        return []
    
    overlap = min(overlap, chunk_size - 1)
    total_length = len(text)
    estimated_chunks = (total_length + chunk_size - overlap - 1) // (chunk_size - overlap)
    
    chunks = []
    start = 0
    chunk_count = 0
    
    while start < total_length:
        end = min(start + chunk_size, total_length)
        chunk = text[start:end]
        chunks.append(chunk)
        
        chunk_count += 1
        progress = (start / total_length) * 100
        logger.info(f"Chunking progress: {progress:.1f}% (Chunk {chunk_count}/{estimated_chunks})")
        
        if end == total_length:
            break
            
        start = end - overlap
        
        if start >= total_length:
            break
    
    logger.info("Chunking completed.")
    return chunks

def process_large_file(file_path: str, buffer_size: int = 1024*1024) -> List[str]:
    """
    Process a large file in streaming mode to avoid memory issues.
    
    Args:
        file_path (str): Path to the large file
        buffer_size (int): Size of each buffer read in bytes
    
    Returns:
        list: A list of text chunks
    """
    chunks = []
    current_chunk = ""
    chunk_size = CONFIG.chunk_size
    overlap = CONFIG.chunk_overlap
    
    try:
        with open(file_path, "r", encoding="utf-8") as file:
            while True:
                buffer = file.read(buffer_size)
                if not buffer:
                    break
                    
                current_chunk += buffer
                
                while len(current_chunk) >= chunk_size:
                    chunks.append(current_chunk[:chunk_size])
                    current_chunk = current_chunk[chunk_size-overlap:]
                    
                logger.info(f"Processed: {len(chunks)} chunks")
            
            if current_chunk:
                chunks.append(current_chunk)
                
        logger.info(f"Completed processing {len(chunks)} chunks from large file.")
        return chunks
        
    except IOError as e:
        logger.error(f"Error processing large file: {e}")
        return chunks
