
import asyncio
import json

import async_timeout

from app.chat.constants import ChatRolesEnum
from app.chat.exceptions import StreamTimeoutException,FailedProcessingException
from app.chat.models import Chunk, Message
from app.core.logs import logger
from app.settings import settings


from app.db import messages_queries
async def stream_generator(subscription):
    async with async_timeout.timeout(5):
        try:
            complete_response: str = ""
            for chunk in subscription:
                # print("chunk:",chunk)
                complete_response = f"{complete_response}{Chunk.get_chunk_delta_content(chunk=chunk)}"
                yield format_to_event_stream(post_processing(chunk))
            message: Message = Message(model=chunk["model"],message=complete_response,role=ChatRolesEnum.ASSISTANT.value)
            messages_queries.insert(model=message.model, message=message.message, role=message.role)
            logger.info(f"Complete Streamed Message: {message}")
        except asyncio.TimeoutError:
            raise StreamTimeoutException
        
def format_to_event_stream(data:str)->str:
    return f"event: message\ndata: {data}\n\n"


def post_processing(chunk) -> str:
    try:
        logger.info(f"Chunk: {chunk}")
        formatted_chunk = Chunk.from_chunk(chunk=chunk)
        logger.info(f"Formmated Chunk: {formatted_chunk}")
        return json.dumps(formatted_chunk.model_dump())
    except Exception:
        raise FailedProcessingException
    

    
