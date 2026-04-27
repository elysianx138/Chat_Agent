import sys
import uvicorn
from contextlib import asynccontextmanager
from pathlib import Path
from fastapi import FastAPI
from api.chat_routers import router as chat_router

ROOT_DIR = Path(__file__).resolve().parent.parent
if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0,str(ROOT_DIR))

@asynccontextmanager
async def lifespan(_:FastAPI):
    yield
    print("√closed successfully")

app = FastAPI(title="RAG-CHAT",version="0.0.1",lifespan=lifespan)

app.include_router(chat_router)

@app.get("/")
async def root():
    return {
        "message":"Hello World"
    }

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)









