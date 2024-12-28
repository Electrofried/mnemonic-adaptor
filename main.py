#!/usr/bin/env python3

import sys
import os

# Local module imports for core functionality
from utils.file_io import save_memory_to_file
from helpers import process_input
from segmentation_agent import segment_input_into_chunks
from memory_extraction_agent import mnemonic_extraction_agent

def main():
    """
    Main entry point for the mnemonic adaptor.
    Processes input text through a pipeline of segmentation and memory extraction.
    
    Example usage:
        python main.py "Some text to parse and store"
        python main.py /path/to/some_file.txt
    
    The pipeline consists of:
    1. Input processing - handles both raw text and file inputs
    2. Text chunking - breaks large inputs into manageable pieces
    3. Segment extraction - identifies key memories in each chunk
    4. Memory processing - converts segments into structured memory objects
    """
    # Validate command line arguments
    if len(sys.argv) < 2:
        script_name = os.path.basename(__file__)
        print(f"Usage: python {script_name} \"Some text or path/to/file\"")
        sys.exit(1)

    # Step 1: Process the input source (file or raw text)
    input_source = sys.argv[1]
    text_chunks = process_input(input_source)
    if not text_chunks:
        print("No text to process.")
        sys.exit(0)

    # Step 2: Process each chunk through the memory pipeline
    for chunk_index, chunk in enumerate(text_chunks, start=1):
        print(f"\n--- Processing Chunk {chunk_index}/{len(text_chunks)} ---")

        # Step 2a: Segment the chunk into potential memories
        segments = segment_input_into_chunks(chunk)
        print(f"[Debug] Segments for Chunk {chunk_index}: {segments}")
        if not segments:
            print(f"No segments returned for chunk {chunk_index}. Moving on.")
            continue

        # Step 2b: Process each segment into a memory object
        for segment_index, item_str in enumerate(segments, start=1):
            print(f"--- Processing Segment {segment_index}/{len(segments)} of Chunk {chunk_index} ---")

            # Extract core memory text, handling both prefixed and unprefixed formats
            prefix = "core_memory:"
            if item_str.startswith(prefix):
                memory_str = item_str[len(prefix):].strip()
            else:
                memory_str = item_str.strip()

            if not memory_str:
                print("Segment has no core memory text after prefix. Skipping.")
                continue

            # Step 2c: Convert the memory text into a structured memory object
            extracted_memory = mnemonic_extraction_agent(
                full_chunk=chunk,
                core_memory_text=memory_str
            )
            print(f"[Debug] Extracted Memory: {extracted_memory}")

            # Step 2d: Save valid memories to storage
            if extracted_memory and extracted_memory.get("memory"):
                save_memory_to_file(extracted_memory)
            else:
                print("No meaningful memory extracted for this segment.")

    print("\nDone processing all chunks.")

if __name__ == "__main__":
    main()
