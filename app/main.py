import sys
import uvicorn
from contextlib import asynccontextmanager
from pathlib import Path
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from api.upload_routers import router as upload_router
from api.chat_routers import router as chat_router
from model.config import Settings as settings

ROOT_DIR = Path(__file__).resolve().parent.parent
if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0,str(ROOT_DIR))

@asynccontextmanager
async def lifespan(_:FastAPI):
    yield
    print("√closed successfully")

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

@app.get("/")
async def root():
    return {
        "messages":f"Hi!{settings.APP_NAME//settings.APP_VERSION}Go to http://127.0.0.1:3000/!",
        "code":200
    }

if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)









