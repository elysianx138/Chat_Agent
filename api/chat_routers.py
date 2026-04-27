
from langchain_core.messages import HumanMessage
from util.get_model import get_model, get_agent
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel,Field

router = APIRouter()

class ChatRequest(BaseModel):
    query: str = Field(min_length=1,description="require that the chat is not NULL")
    session_id: str = "default"


agent = get_agent()
@router.post("/chat")
def chat(payload: ChatRequest):
    try:
        response = agent.invoke(
            {
                "message": [
                   HumanMessage(content=payload.query),
                ]
            },
            config={"configurable":{"thread_id":payload.session_id} },
        )

    except Exception as err:
        error_name = err.__class__.__name__
        # 获取报错类型名称
        if error_name == "AttributeError":
            raise HTTPException(
                status_code=502,
                detail=(
                    f"API过期或者已经失效."
                    f"请检查或者更新您的API"
                )
            ) from err

        raise HTTPException(
            status_code=500,
            detail=(
                f"执行失败!{error_name}"
            )
        ) from err

    return {
        "answer":response["message"][-1],
        "session_id":payload.session_id,
        "debug_content":response["context",""],
    }


