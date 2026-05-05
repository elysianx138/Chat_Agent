from langchain_text_splitters import RecursiveCharacterTextSplitter

"""
文本的切割
====================
 - splitter(docs):将文本docs切割目标字符数,且字符数块之间的重叠为20!
"""
def splitter(docs):
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=500,
        chunk_overlap=100,
    )
    text = splitter.split_documents(docs)
    return text
