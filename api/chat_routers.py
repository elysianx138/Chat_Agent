from fastapi import APIRouter, HTTPException
from langchain_core.messages import HumanMessage
from pydantic import BaseModel, Field

from util.get_model import get_agent

router = APIRouter()


class ChatRequest(BaseModel):
    query: str = Field(min_length=1, description="require that the chat is not NULL")
    session_id: str = "default"


agent = get_agent()


@router.post("/chat")
def chat(payload: ChatRequest):
    try:
        response = agent.invoke(
            {
                "messages": [
                    HumanMessage(content=payload.query),
                ]
            },
            config={"configurable": {"thread_id": payload.session_id}},
        )
    except Exception as err:
        error_name = err.__class__.__name__
        if error_name == "AttributeError":
            raise HTTPException(
                status_code=502,
                detail="AI API call failed. Please verify API key/base URL/model.",
            ) from err

        raise HTTPException(
            status_code=500,
            detail=f"Chat execution failed: {error_name}: {str(err)}",
        ) from err

    messages = response.get("messages", [])
    # answer = messages[-1].content if messages else ""

    return {
        "answer": messages[-1].content,
        "session_id": payload.session_id,
        "debug_content": response.get("context", ""),
    }
