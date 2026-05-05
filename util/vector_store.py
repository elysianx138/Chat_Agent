import numpy as np
from functools import lru_cache
from langchain_community.vectorstores import Chroma

from util.get_embeddings import get_embeddings

@lru_cache(maxsize=1)
def get_embeddings_model():
    embeddings = get_embeddings()
    return embeddings

def get_vector_store(text):
    embeddings = get_embeddings_model()
    vector_store = Chroma.from_documents(text,embeddings)
    return vector_store

