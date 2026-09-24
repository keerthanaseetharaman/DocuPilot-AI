def create_chunks(pages, chunk_size=1000, overlap=200):
    """
    Split extracted PDF text into smaller chunks.

    pages format:
    [
        {
            "page": 1,
            "text": "..."
        }
    ]
    """

    chunks = []

    for page in pages:

        page_number = page["page"]
        text = page["text"].strip()

        if not text:
            continue

        start = 0

        while start < len(text):

            end = start + chunk_size

            chunk_text = text[start:end]

            chunks.append({
                "page": page_number,
                "text": chunk_text
            })

            start += chunk_size - overlap

    return chunks