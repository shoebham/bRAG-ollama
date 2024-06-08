

from fastapi import APIRouter

import openai

from app.chat.exceptions import OpenAIException 
from app.chat.models import BaseMessage,Message
from app.chat.services import OpenAIService
from starlette.responses import StreamingResponse

router = APIRouter(tags = ["Core Endpoints"])

@router.post("/v1/completion")
async def completion_create(input_message:BaseMessage) -> Message:
    try:
        return await OpenAIService.chat_completion(input_message=input_message)
    except openai.OpenAIError:
        print("Excpetion")
        raise OpenAIException
    

@router.post("/v1/completion-stream")
async def completion_stream(input_message:BaseMessage) -> StreamingResponse:
    try:
        return await OpenAIService.chat_completion_with_streaming(input_message=input_message)
    except:
        raise OpenAIException
