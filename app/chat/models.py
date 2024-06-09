

from pydantic import BaseModel, Field


from app.chat.constants import ChatRolesEnum,ModelsEnum

from app.chat.exceptions import FailedProcessingException
from app.core.models import TimestampAbstractModel


class BaseMessage(BaseModel):
    "Base pydantic model used to interact with api"
    model :ModelsEnum = Field(default=ModelsEnum.LLAMA3.value) 
    message:str
    

class Message(TimestampAbstractModel,BaseMessage):
    role: ChatRolesEnum


class Message(BaseMessage):
    role: ChatRolesEnum



class Chunk(BaseModel):
    model: ModelsEnum = Field(default=ModelsEnum.LLAMA3.value)
    content: str
    created_at:str
    finish:bool| None = None

    @staticmethod
    def get_chunk_delta_content(chunk:dict | str) ->str:
        try:
            match chunk:
                case str(chunk):
                    return chunk
                case dict(chunk):
                    return chunk['message']['content']
        except Exception as e:
            raise FailedProcessingException


    @classmethod
    def from_chunk(cls,chunk):
        delta_content: str = cls.get_chunk_delta_content(chunk=chunk)
        return cls(
            created_at=chunk["created_at"],
            model=chunk["model"],
            content=delta_content,
            finish=chunk['done']
            )