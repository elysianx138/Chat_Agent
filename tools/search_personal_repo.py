from langchain_core.tools import tool
from dotenv import load_dotenv
from tools import get_knowledge_base
load_dotenv()

@tool
def search_personal_repo(query:str) -> str:
    """当用户输入/doc或者想要查询或者你需要查看用户知识库的时候,进行调用;并给用户说明你查询了用户的哪个知识库,哪个文件!并根据相关内容进行解释说明
    """

    vector_store = get_knowledge_base()
    if vector_store is None:
        return "知识库未初始化，请先上传文件"
    results = vector_store.similarity_search(query, k=2)
    if not results:
        return "未找到相关内容"
    return "\n\n".join([doc.page_content for doc in results])