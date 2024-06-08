

import openai

from openai.types.chat import ChatCompletion

from app.chat.constants import ChatRolesEnum
from app.chat.models import BaseMessage,Message
from app.core.logs import logger
from app.settings import settings
from starlette.responses import StreamingResponse

import ollama

openai_client = openai.AsyncOpenAI(api_key=settings.OPENAI_API_KEY)


class OpenAIService:
    @classmethod    
    async def chat_completion(cls,input_message:BaseMessage) ->  Message:
        logger.info(f"Recieved the following completion: {input_message}")
        completion: str = ollama.chat(model=input_message.model,messages=[
            {
                'role':'user',
                'content':'Why is the sky blue?',
            }
        ])
        logger.info(f"Got the following Response: {completion}")
        return Message(
            model = input_message.model,
            role = "user",
            message=completion['message']['content'],
        )

    @staticmethod
    async def chat_completion_with_streaming(input_message:BaseMessage) -> StreamingResponse:
        subscription: ChatCompletion = await openai_client.chat.completions.create(
              model = input_message.model,
            messages = [{"role":ChatRolesEnum.ASSISTANT.value,"content":input_message.message}],
            stream=True
        )
    @staticmethod
    def extract_response_from_completion(chat_completion:ChatCompletion) -> str:
        return chat_completion.choices[0].message.content