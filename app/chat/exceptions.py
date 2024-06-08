# chats/exceptions.py
# here we define some exceptions that will come handy in the future
from fastapi import HTTPException
from starlette import status

from app.chat.constants import FailureReasonsEnum


class OpenAIException(HTTPException):
    def __init__(self):
        super().__init__(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=FailureReasonsEnum.OPENAI_ERROR.value)


class OpenAIFailedProcessingException(HTTPException):
    def __init__(self):
        super().__init__(status_code=status.HTTP_503_SERVICE_UNAVAILABLE, detail=FailureReasonsEnum.FAILED_PROCESSING.value)


class OpenAIStreamTimeoutException(HTTPException):
    def __init__(self):
        super().__init__(status_code=status.HTTP_504_GATEWAY_TIMEOUT, detail=FailureReasonsEnum.STREAM_TIMEOUT.value)


class RetrievalNoDocumentsFoundException(HTTPException):
    def __init__(self):
        super().__init__(status_code=status.HTTP_404_NOT_FOUND, detail=FailureReasonsEnum.NO_DOCUMENTS_FOUND.value)
