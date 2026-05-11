import os
from pathlib import Path
from langchain_community.document_loaders import DirectoryLoader

DATA_DIR = Path(os.getenv("UPLOAD_DIR","uploadsads"))
DATA_DIR.mkdir(parents=True, exist_ok=True)

"""
文件的加载
================
 - load_files():加载指定文件(text.text)

"""

def load_files():
    loader = DirectoryLoader(DATA_DIR,glob="*.md")
    docs = loader.load()
    return docs