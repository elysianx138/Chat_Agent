from langchain.agents import create_agent
from langchain_openai import ChatOpenAI
from dotenv import load_dotenv
import os

from langgraph.checkpoint.memory import MemorySaver

load_dotenv()

def get_model():
    return ChatOpenAI(
        model = os.getenv("AI_MODEL","gpt-3.5-turbo"),
        base_url= os.getenv("BASE_URL","https://api.openai.com/v1"),
        api_key= os.getenv("API_KEY","sk-test"),
    )
def get_agent():
    model = get_model()
    memory = MemorySaver()
    return create_agent(
        model = model,
        checkpointer= memory,
        system_prompt="you are very kind and can understand what the user says in a friendly way"
    )