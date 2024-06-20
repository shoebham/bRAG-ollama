

from fastapi import APIRouter

from app.chat.exceptions import APIException 
from app.chat.models import BaseMessage,Message
from app.chat.services import OllamaService
from starlette.responses import StreamingResponse
from app.db import messages_queries

router = APIRouter(tags = ["Core Endpoints"])

@router.post("/v1/completion")
async def completion_create(input_message:BaseMessage) -> Message:
    try:
        return await OllamaService.chat_completion(input_message=input_message)
    except Exception as e:
        print(f"Excpetion: {e}")
        raise APIException
    

@router.post("/v1/completion-stream")
async def completion_stream(input_message:BaseMessage) -> StreamingResponse:
    try:
        return await OllamaService.chat_completion_with_streaming(input_message=input_message)
    except:
        raise APIException


@router.post("/v1/qa-create")
async def qa_create(input_message: BaseMessage) -> Message:
    try:
        return await OllamaService.qa_without_stream(input_message=input_message)
    except:
        raise APIException


@router.post("/v1/qa-create-pdf")
async def qa_create(input_message: BaseMessage) -> Message:
    try:
        return await OllamaService.qa_without_stream(input_message=input_message,isPdf=True)
    except:
        raise APIException

@router.post("/v1/qa-create-pdf-stream")
async def qa_create(input_message: BaseMessage) -> Message:
    try:
        return await OllamaService.qa_with_stream(input_message=input_message,isPdf=True)
    except:
        raise APIException
    
@router.get("/v1/messages")
async def get_messages() -> list[Message]:
    return [Message(**message) for message in messages_queries.select_all()]