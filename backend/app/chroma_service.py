import chromadb

# Create ChromaDB client
client = chromadb.PersistentClient(path="chroma_db")

# Create or get collection
collection = client.get_or_create_collection(
    name="documents"
)


def store_chunks(chunks, embeddings, document_name):
    """
    Store document chunks and their embeddings in ChromaDB.
    """

    ids = []
    documents = []
    metadatas = []

    for index, chunk in enumerate(chunks):
        ids.append(f"{document_name}_{index}")

        documents.append(chunk["text"])

        metadatas.append({
            "document": document_name,
            "page": chunk["page"]
        })

    collection.add(
        ids=ids,
        documents=documents,
        embeddings=embeddings,
        metadatas=metadatas
    )

    return len(ids)