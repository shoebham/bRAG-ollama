# settings/__init__.py
from app.settings.base import Settings
from pydantic import BaseModel, ValidationError

settings = Settings()
