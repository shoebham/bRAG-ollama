
from pydantic import Field

from pydantic_settings import BaseSettings

from app.core.constants import Environments

class Settings(BaseSettings):
    APP_NAME:str = "bRAG"
    ENVIRONMENT:str = Field(env = "ENVIRONMENT",default=Environments.LOCAL.value)
    OPENAI_API_KEY: str = Field(env="OPENAI_API_KEY", default="None")
    GENERATION_TIMEOUT_SEC: int = Field(env="GENERATION_TIMEOUT_SEC", default=5)
    DATABASE_URL: str = Field(env="DATABASE_URL",default="None")

    QDRANT_HOST: str = Field(env = "QDRANT_HOST",default="qdrant")
    QDRANT_PORT: int = Field(env = "QDRANT_PORT",default=6333)
    QDRANT_COLLECTION_NAME: str = Field(env = "QDRANT_COLLECTION_NAME",default="demo")
 

    @property
    def is_local(self):
        return self.ENVIRONMENT == Environments.LOCAL.value
    
    class Config:
        env_file = ".env"

