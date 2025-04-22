from langchain_openai import OpenAIEmbeddings
import dotenv
import os
from langchain_community.vectorstores import FAISS
from langchain.tools import Tool


####NOT IN USE OLD VERSION####

def buscar_contexto(query: str) -> str:
    dotenv.load_dotenv('../.env')
    api_key = os.getenv("API_KEY_OPENAI")
    os.environ["OPENAI_API_KEY"] = api_key
    # Paso 1: Configurar el vectorstore como herramienta de búsqueda
    embeddings = OpenAIEmbeddings(model="text-embedding-3-small")  # o "text-embedding-ada-002"
    db = FAISS.load_local("./data/faiss_news_index/", embeddings=embeddings, allow_dangerous_deserialization=True)
    retriever = db.as_retriever()
    docs = retriever.invoke(query,k=15)
    return "\n\n".join([
        f"Título: {doc.metadata.get('title', 'N/A')}\n"
        f"Fuente: {doc.metadata.get('source', 'N/A')}\n"
        f"URL: {doc.metadata.get('url', 'N/A')}\n"
        f"Contenido: {doc.page_content}"
        for doc in docs
    ])

def search_tool():
    herramienta_busqueda = Tool(
        name="SearchNews",
        func=buscar_contexto,
        description="useful for searching news articles and financial information. "
    )
    return herramienta_busqueda