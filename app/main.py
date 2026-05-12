import sys
import logging
import uvicorn
from datetime import datetime
from contextlib import asynccontextmanager
from dotenv import load_dotenv
from pathlib import Path
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from api.upload_routers import router as upload_router
from api.chat_routers import router as chat_router
from MCP.search_mcp import search_website
from model.config import Settings as settings

ROOT_DIR = Path(__file__).resolve().parent.parent
if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0,str(ROOT_DIR))

logger = logging.getLogger("uvicorn")

load_dotenv()
@asynccontextmanager
async def lifespan(_:FastAPI):
    logger.info('='*60)
    logger.info(f"🌐  name:{settings.APP_NAME},🚀  version:{settings.APP_VERSION},⏰  start:{datetime.now()}")

    try:
        await search_website()
        logger.info("Dependencies initialized")
    except Exception as e:
        logger.critical(f"Dependencies not initialized: {e}")
        raise

    yield
    logger.info('='*60)
    logger.info("Closed successfully")

app = FastAPI(title="RAG-CHAT",version="0.0.1",lifespan=lifespan)

# === CORS跨域访问后端 ===
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(chat_router)
app.include_router(upload_router)

# cd C:\Users\shiko\Desktop\RAG-CHAT-learn\ui
# python -m http.server 3000

@app.get("/")
async def root():
    return {
        "messages":"Hi!Contact successfully!Go to http://127.0.0.1:3000/!",
        "code":200
    }

if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)









