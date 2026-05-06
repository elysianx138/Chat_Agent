from langchain.agents import create_agent
from langchain_openai import ChatOpenAI
import os
from langgraph.checkpoint.memory import MemorySaver
from tools.search_personal_repo import search_personal_repo
from MCP.mcp_stores import mcp_tools


def get_model():
    return ChatOpenAI(
        model = os.getenv("AI_MODEL","qwen-plus"),
        base_url= os.getenv("BASE_URL","https://dashscope.aliyuncs.com/compatible-mode/v1"),
        api_key= os.getenv("API_KEY"),
        temperature=0.7,
    )

def get_agent():
    model = get_model()
    memory = MemorySaver()
    return create_agent(
        model = model,
        checkpointer= memory,
        tools=[search_personal_repo] + mcp_tools,
        system_prompt="you are very kind and can understand what the user says in a friendly way."
    )