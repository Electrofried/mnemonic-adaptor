def split_text_with_overlap(text, chunk_size=2000, overlap=200):
    """
    Example chunking function that splits text into chunks of `chunk_size`,
    with an `overlap` of tokens/characters between chunks.
    """
    chunks = []
    start = 0
    while start < len(text):
        end = start + chunk_size
        chunk = text[start:end]
        chunks.append(chunk)
        start = end - overlap
        if start < 0:
            start = 0
    return chunks
