from app.chroma_service import collection


def search_documents(query, top_k=3):
    """
    Search the most relevant document chunks
    from ChromaDB.
    """

    results = collection.query(
        query_texts=[query],
        n_results=top_k
    )

    documents = results.get("documents", [[]])[0]
    metadatas = results.get("metadatas", [[]])[0]

    search_results = []

    for document, metadata in zip(documents, metadatas):
        search_results.append({
            "text": document,
            "document": metadata.get("document"),
            "page": metadata.get("page")
        })

    return search_results