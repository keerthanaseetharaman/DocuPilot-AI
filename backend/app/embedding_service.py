from sentence_transformers import SentenceTransformer

# Load embedding model
model = SentenceTransformer("all-MiniLM-L6-v2")


def create_embeddings(texts):
    """
    Convert text chunks into numerical embeddings.
    """

    embeddings = model.encode(texts)

    return embeddings.tolist()