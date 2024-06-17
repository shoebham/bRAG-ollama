

# import openai

# from openai.types.chat import ChatCompletion

from ollama import Client
from app.chat.constants import ChatRolesEnum
from app.chat.exceptions import RetrievalNoDocumentsFoundException
from app.chat.models import BaseMessage,Message
from app.core.logs import logger
from app.settings import settings
from starlette.responses import StreamingResponse
from app.chat.constants import ChatRolesEnum, NO_DOCUMENTS_FOUND
from app.chat.retrievals import process_retrieval
from app.chat.streaming import stream_generator

# openai_client = openai.AsyncOpenAI(api_key=settings.OPENAI_API_KEY)

from async_generator import async_generator, yield_

from app.db import messages_queries
import os
client = Client(host="http://host.docker.internal:11434")
class OllamaService:
    @classmethod    
    async def chat_completion(cls,input_message:BaseMessage) ->  Message:
        logger.info(f"Recieved the following completion: {input_message}")
        completion: str = client.chat(model=input_message.model,messages=[
            {
                'role':'user',
                'content': input_message.message
            }
        ])
        logger.info(f"Got the following Response: {completion}")
        message = Message(
            model = input_message.model,
            role = "user",
            message=completion['message']['content'],
        )
        messages_queries.insert(model=message.model,message=message.model,role=message.role)
        return message
        
    
    @staticmethod
    async def chat_completion_with_streaming(input_message:BaseMessage) -> StreamingResponse:
        subscription= client.chat(
              model = input_message.model,
            messages = [{"role":ChatRolesEnum.USER.value,"content":input_message.message}],
            stream=True
        )

        @staticmethod
        async def async_generator_wrapper(sync_gen):
            for item in sync_gen:
                yield item
        return StreamingResponse(stream_generator(async_generator_wrapper(subscription)),media_type="text/event-stream")


    @staticmethod
    def extract_response_from_completion(chat_completion:dict) -> str:
        return chat_completion.choices[0].message.content
    

    @classmethod
    async def qa_without_stream(cls,input_message: BaseMessage) -> Message:
        try:
            augmented_message: BaseMessage = process_retrieval(message=input_message)
            print(f"Augemented Message: {augmented_message}")
            return await cls.chat_completion(input_message=augmented_message)
        except RetrievalNoDocumentsFoundException:
            return Message(model=input_message.model, message=NO_DOCUMENTS_FOUND, role=ChatRolesEnum.ASSISTANT.value)