
from enum import StrEnum

class FailureReasonsEnum(StrEnum):
    API_ERROR = "API call failed"
    STREAM_TIMEOUT = "Stream timed out"
    FAILED_PROCESSING = "Post Processing Failed"
    NO_DOCUMENTS_FOUND = "No Documents Found"

class ChatRolesEnum(StrEnum):
    USER = "user"
    SYSTEM = "system"
    ASSISTANT = "assistant"

class ModelsEnum(StrEnum):
    GPT4 = "gpt-4-0613"
    LLAMA3= "llama3"

