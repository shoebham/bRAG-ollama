

from fastapi import FastAPI

from app import version
from app.core.logs import logger
from app.core.api import router as core_router
from app.chat.api import router as chat_router
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware

app  = FastAPI(version=version)
# Mount the directory containing your HTML file
app.mount("/Users/shubhamgupta/Desktop/my-stuff/projects/bRAG/static", StaticFiles(directory="static"), name="static")

origins = ["*"]
from fastapi import Request
from fastapi.responses import JSONResponse
@app.middleware("http")
async def log_requests(request: Request, call_next):
    try:
        response = await call_next(request)
        return response
    except Exception as e:
        print(f"Unhandled exception: {str(e)}")
        return JSONResponse(status_code=500, content={"detail": "Internal Server Error"})

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
    
app.include_router(core_router)
app.include_router(chat_router)

logger.info("App is ready....")


