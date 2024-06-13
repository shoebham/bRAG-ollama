
from qdrant_client import QdrantClient

from app.settings import settings

def test_populate_vector_db(client: QdrantClient):
    docs = (
        "LoremIpsum sit dolorem",
        "Completely random phrase",
        "Another random phrase",
        "shubham is awesome.",
    )

    metadata = (
        {"source":"Olaf"},
        {"source":"grski"},
        {"source":"Olaf"},
        {"source":"grski"},
    )

    ids = [42,2,3,5]

    client.add(
        collection_name=settings.QDRANT_COLLECTION_NAME,
        documents=docs,
        metadata=metadata,
        ids=ids
    )