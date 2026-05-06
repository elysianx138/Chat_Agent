import os
from langchain_community.embeddings import DashScopeEmbeddings


def get_embeddings():

    return DashScopeEmbeddings(
        model=os.getenv("AI_EMBEDDING_MODEL", "text-embedding-v3"),
        dashscope_api_key=os.getenv("API_KEY")
    )

