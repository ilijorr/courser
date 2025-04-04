from fastapi import HTTPException, Request, status
from langchain_core.vectorstores import VectorStore
from pinecone import Pinecone
from core.settings import PineconeSettings, SettingsFactory

from langchain_pinecone import PineconeVectorStore

from .embeddings import azure

settings = SettingsFactory.create(PineconeSettings)
def init_pinecone() -> PineconeVectorStore:
    pc = Pinecone(api_key=settings.api_key)
    index_name = settings.index_name

    if index_name not in pc.list_indexes().names():
        raise ValueError(f"pinecone index {index_name} not found")

    index = pc.Index(index_name)
    # index.delete(delete_all=True)

    return PineconeVectorStore(
            index=index,
            embedding=azure.get_embeddings())

def get_db(request: Request) -> VectorStore:
    if not hasattr(request.app.state, "vectorstore"):
        raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="vector store not initialized"
                )
    return request.app.state.vectorstore
