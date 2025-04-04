from contextlib import asynccontextmanager
from fastapi import FastAPI

from api.v1 import v1_router
from vec_db.pinecone import init_pinecone
from rel_db import postgres

@asynccontextmanager
async def lifespan(app: FastAPI):
    postgres.create_db_and_tables()
    app.state.vectorstore = init_pinecone()
    yield
    postgres.engine.dispose()

app = FastAPI(lifespan=lifespan)

app.include_router(v1_router)

@app.get("/")
async def root():
    return {"message": "hello world"}
