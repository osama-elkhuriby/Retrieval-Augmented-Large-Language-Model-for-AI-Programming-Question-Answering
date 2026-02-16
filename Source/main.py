"""
this our Rag applicaition for CS-810 course at University of Queen's in Canada. The main.py file is the entry point of our application where we initialize the FastAPI app, set up database connections, and include our route handlers for different endpoints.

Team Members:
1. Nematalla, Esraa - 20592811
2. Elkhuribi, Osama - 20596292   

Date: 2026-02-04

"""
from fastapi import FastAPI
from routes import base, data
from motor.motor_asyncio import AsyncIOMotorClient
from helpers.config import get_settings
from stores.llm.LLMProviderFactory import LLMProviderFactory


app = FastAPI()


@app.on_event("startup")
async def startup_db_client():
    settings = get_settings()
    app.mongodb_client = AsyncIOMotorClient(settings.MONGODB_URL)
    app.mongodb = app.mongodb_client[settings.MONGODB_DATABASE]

    llm_provider_factory = LLMProviderFactory(settings)

    # generation client
    app.generation_client = llm_provider_factory.create(provider=settings.GENERATION_BACKEND)
    app.generation_client.set_generation_model(model_id = settings.GENERATION_MODEL_ID)

    # embedding client
    app.embedding_client = llm_provider_factory.create(provider=settings.EMBEDDING_BACKEND)
    app.embedding_client.set_embedding_model(model_id=settings.EMBEDDING_MODEL_ID,
                                             embedding_size=settings.EMBEDDING_MODEL_SIZE)

@app.on_event("shutdown")
async def shutdown_db_client():
    app.mongodb_client.close()


app.router.lifespan.on_startup.append(startup_db_client)
app.router.lifespan.on_shutdown.append(shutdown_db_client)


app.include_router(base.base_router)
app.include_router(data.data_router)





