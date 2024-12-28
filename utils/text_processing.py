"""
Text processing utilities for chunking and handling large text inputs.
"""

from config import CONFIG
from utils import utils

@utils
def split_text_with_overlap(text, chunk_size=2000, overlap=200):
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
        print(f"\rChunking progress: {progress:.1f}% (Chunk {chunk_count}/{estimated_chunks})", end="", flush=True)
        
        if end == total_length:
            break
            
        start = end - overlap
        
        if start >= total_length:
            break
    
    print("\nChunking completed.")
    return chunks

@utils
def process_large_file(file_path, buffer_size=1024*1024):
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
    chunk_size = CONFIG["CHUNK_SIZE"]
    overlap = CONFIG.get("CHUNK_OVERLAP", 200)
    
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
                    
                print(f"\rProcessed: {len(chunks)} chunks", end="", flush=True)
            
            if current_chunk:
                chunks.append(current_chunk)
                
        print(f"\nCompleted processing {len(chunks)} chunks from large file.")
        return chunks
        
    except IOError as e:
        print(f"Error processing large file: {e}")
        return chunks 