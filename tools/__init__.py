from util.vector_store import get_vector_store
from util.load_files import load_files
from util.splitter import splitter

_knowledge_base = None

def get_knowledge_base():
    global _knowledge_base
    if _knowledge_base is None:
        reload_knowledge_base()
    return _knowledge_base

def reload_knowledge_base():
    global _knowledge_base
    _knowledge_base = None
    docs = load_files()
    if docs:
        text = splitter(docs)
        _knowledge_base = get_vector_store(text)
    return _knowledge_base