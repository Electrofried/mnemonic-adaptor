#!/usr/bin/env python3

import sys
import os

# Local module imports
from helpers import process_input, save_memory_to_file
from segmentation_agent import segment_input_into_chunks
from memory_extraction_agent import mnemonic_extraction_agent

def main():
    """
    Example usage:
        python main.py "Some text to parse and store"
        python main.py /path/to/some_file.txt
    """
    if len(sys.argv) < 2:
        script_name = os.path.basename(__file__)
        print(f"Usage: python {script_name} \"Some text or path/to/file\"")
        sys.exit(1)

    input_source = sys.argv[1]
    text_chunks = process_input(input_source)
    if not text_chunks:
        print("No text to process.")
        sys.exit(0)

    # Process each chunk
    for chunk_index, chunk in enumerate(text_chunks, start=1):
        print(f"\n--- Processing Chunk {chunk_index}/{len(text_chunks)} ---")

        # (a) Segment the chunk
        segments = segment_input_into_chunks(chunk)
        print(f"[Debug] Segments for Chunk {chunk_index}: {segments}")
        if not segments:
            print(f"No segments returned for chunk {chunk_index}. Moving on.")
            continue

        # (b) For each segment, parse out the text after "core_memory:"
        for segment_index, item_str in enumerate(segments, start=1):
            print(f"--- Processing Segment {segment_index}/{len(segments)} of Chunk {chunk_index} ---")

            prefix = "core_memory:"
            if item_str.startswith(prefix):
                memory_str = item_str[len(prefix):].strip()
            else:
                memory_str = item_str.strip()

            if not memory_str:
                print("Segment has no core memory text after prefix. Skipping.")
                continue

            # (c) Extract the memory
            extracted_memory = mnemonic_extraction_agent(
                full_chunk=chunk,
                core_memory_text=memory_str
            )
            print(f"[Debug] Extracted Memory: {extracted_memory}")

            # Collect if we have a real memory
            if extracted_memory and extracted_memory.get("memory"):
                save_memory_to_file(extracted_memory)
            else:
                print("No meaningful memory extracted for this segment.")

    print("\nDone processing all chunks.")

if __name__ == "__main__":
    main()
