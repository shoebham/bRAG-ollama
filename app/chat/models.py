

from pydantic import BaseModel, Field


from app.chat.constants import ChatRolesEnum,ModelsEnum

from app.core.models import TimestampAbstractModel


class BaseMessage(BaseModel):
    "Base pydantic model used to interact with api"
    model :ModelsEnum = Field(default=ModelsEnum.GPT4.value) 
    message:str
    

class Message(TimestampAbstractModel,BaseMessage):
    role: ChatRolesEnum


class Message(BaseMessage):
    role: ChatRolesEnum


