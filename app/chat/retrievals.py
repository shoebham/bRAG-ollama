

from qdrant_client import QdrantClient

from app.chat.models import BaseMessage 

from app.chat.exceptions import RetrievalNoDocumentsFoundException 
from app.settings import settings
from app.chat.ingest import test_populate_vector_db

from app.chat.readPdf import start
from app.core.logs import logger
import openai   


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


def process_retrieval_pdf(message: BaseMessage) -> BaseMessage:
    """Return top3 similar documents"""
    search_result = search_pdf(query = message.message,collection_name="pdfs")
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
    res = "\n".join(result["payload"]["text"] for result in search_result)
    logger.info(f"Res: {res}")
    return res


def search_pdf(query:str,collection_name:str) -> str:
    start(client=client)
    from app.chat.services import ollama_client
    response= ollama_client.embeddings(
        model='mxbai-embed-large',
        prompt='text_chunks',
        )

    embeddings = response["embedding"]
    search_result = client.search(
        collection_name=collection_name,
        query_vector=embeddings,
        limit=3
    )
    print(f"Search Result: {search_result}\n")
    if not search_result:
        raise RetrievalNoDocumentsFoundException 
    for result in search_result:
        print(f"Result: result['payload']")
    res = "\n".join(result.payload["text"] for result in search_result)
    logger.info(f"Res: {res}")
    return res
