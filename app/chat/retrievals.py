

from qdrant_client import QdrantClient

from app.chat.models import BaseMessage 

from app.chat.exceptions import RetrievalNoDocumentsFoundException 
from app.settings import settings
from app.chat.ingest import test_populate_vector_db

from app.core.logs import logger


client = QdrantClient(settings.QDRANT_HOST,port=settings.QDRANT_PORT)

# test_populate_vector_db(client=client)


def process_retrieval(message: BaseMessage) -> BaseMessage:
    """Return top3 similar documents"""
    search_result = search(query = message.message)
    resulting_query : str = (
        f"Answer Based on only context,nothing else\n"
        f"QUERY:\n{message.message}\n"
        f"CONTEXT:\n{search_result}\n"
    )
    logger.info(f"Resulting Query: {resulting_query}\n")
    return BaseMessage(message=resulting_query,model=message.model)


def search(query:str) -> str:
    search_result = client.query(collection_name=settings.QDRANT_COLLECTION_NAME,limit=3,query_text=query)
    print(f"Search Result: {search_result}\n")
    if not search_result:
        raise RetrievalNoDocumentsFoundException 
    return "\n".join(result.document for result in search_result)