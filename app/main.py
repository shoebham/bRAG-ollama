

from fastapi import FastAPI

from app import version
from app.core.logs import logger
from app.core.api import router as core_router
from app.chat.api import router as chat_router
from fastapi.staticfiles import StaticFiles

app  = FastAPI(version=version)
# Mount the directory containing your HTML file
app.mount("/Users/shubhamgupta/Desktop/my-stuff/projects/bRAG/static", StaticFiles(directory="static"), name="static")


    
app.include_router(core_router)
app.include_router(chat_router)

logger.info("App is ready....")


